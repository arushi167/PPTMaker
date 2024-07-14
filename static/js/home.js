document.addEventListener('DOMContentLoaded', function() {
    var topicInput = document.getElementById('topic');
    var characterCount = document.getElementById('text_count');
    var topic_message = document.getElementById("topic_message");
    var submitBtn = document.getElementById("submit_btn");
    var try_again_btn = document.getElementById("try_again_btn");
    var continue_btn = document.getElementById("continue_btn");
    var topic_message_div = document.getElementById("topic_message_div");
    var loading_div = document.getElementById("loading_div");

    topicInput.addEventListener('input', function() {
        var maxLength = 200;
        var currentLength = topicInput.value.length;

        if (currentLength > maxLength) {
            topicInput.value = topicInput.value.substring(0, maxLength);
            currentLength = maxLength;
        }

        // Update the character count
        characterCount.textContent = currentLength + '/' + maxLength;
        topic_message.innerHTML = topicInput.value+"? Intriguing! <br>Allow me to brainstorm some concepts..."

        document.getElementById("topic_message_div").classList.add("d-none");
        document.getElementById("success_content_msg").classList.add("d-none");
        document.getElementById("content_box").innerHTML = "";
        document.getElementById("content_box_div").classList.add("d-none");
        document.getElementById("inform_image_div").classList.add("d-none");
        document.getElementById("success_image_div").classList.add("d-none");
        document.getElementById("image_box_div").classList.add("d-none");
        document.getElementById("success_div").classList.add("d-none");
    });

    topicInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            topic_message_div.classList.remove("d-none");
            generateContent();
        }
    });

    submitBtn.addEventListener("click", function() {
        topic_message_div.classList.remove("d-none");
        generateContent();
    });

    try_again_btn.addEventListener("click", function() {
        document.getElementById("success_content_msg").classList.add("d-none");
        document.getElementById("content_box").innerHTML = "";
        document.getElementById("content_box_div").classList.add("d-none");
        generateContent();
    });

    continue_btn.addEventListener("click", function() {
        generateImages();
    });

    function generateContent() {
        loading_div.classList.remove("d-none");
        const content_box = document.getElementById("content_box");
        const contentDiv = document.getElementById("content_box_div");
        const content_action_btn = document.getElementById("content_action_btn");
        let htmlBuffer = "";  // Buffer to store partial HTML content

        const topic = topicInput.value;
        const slidecount = 7; // Set your slide count here

        const eventSource = new EventSource(`/content?topic=${encodeURIComponent(topic)}&slidecount=${slidecount}`);

        eventSource.onmessage = function(event) {
            const message = event.data;

            if (message === "Session Terminated") {
                eventSource.close();
                loading_div.classList.add("d-none");
                document.getElementById("success_content_msg").classList.remove("d-none");
                content_action_btn.classList.remove("d-none");
                
                const jsonContent = convertHTMLToJSON();
                localStorage.setItem('json_data', JSON.stringify(jsonContent));
                console.log(jsonContent);
            } else {
                // Append the received message to the buffer
                htmlBuffer += message;

                // Check if the buffer contains complete <div> tags
                const completeULRegex = /<div>.*?<\/div>/gs;
                let match = completeULRegex.exec(htmlBuffer);

                while (match !== null) {
                    // Append complete <div> tag to the content_box
                    content_box.insertAdjacentHTML('beforeend', match[0]);

                    contentDiv.classList.remove("d-none");

                    // Append <br> tag after <ul> tag
                    content_box.insertAdjacentHTML('beforeend', '<br>');

                    // Scroll the Context Box to Bottom
                    content_box.scrollTop = content_box.scrollHeight;

                    // Update the buffer, removing the processed <div> tag
                    htmlBuffer = htmlBuffer.slice(match.index + match[0].length);

                    // Find the next match in the updated buffer
                    match = completeULRegex.exec(htmlBuffer);
                }
            }
        };
    }

    function convertHTMLToJSON() {
        const contentBox = document.getElementById("content_box");
        const ulElements = contentBox.querySelectorAll('div');
        const contentArray = [];
    
        var index = 1
        ulElements.forEach((ulElement) => {
            const liElements = ulElement.querySelectorAll('li');
            const slide = index;
            const heading = liElements[1].textContent.trim();
            const slideContent = liElements[2].textContent.trim();
    
            contentArray.push({
                slide: slide,
                heading: heading,
                slidecontent: slideContent
            });
            index += 1;
        });
    
        const jsonContent = {
            content: contentArray
        };
    
        return jsonContent;
    }

    // Generate Images Code
    try_again_image_btn.addEventListener("click", function() {
        generateImages();
    });

    continue_image_btn.addEventListener("click", function() {
        document.getElementById("inform_ppt_div").classList.remove("d-none");
        document.getElementById("loading_ppt_div").classList.remove("d-none");
        generatePPT();
    });

    function generateImages() {
        document.getElementById("inform_image_div").classList.remove("d-none");
        document.getElementById("loading_img_div").classList.remove("d-none");
        document.getElementById("image_box").innerHTML = "";
        var topic = topicInput.value;
        var raw_jsonData = localStorage.getItem('json_data');
        var jsonData = JSON.parse(raw_jsonData);

        fetch('/images', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'topic=' + encodeURIComponent(topic) + '&json_data=' + encodeURIComponent(raw_jsonData)
        })
        .then(function(response) {
            return response.json(); 
        })
        .then(function(data) {
            console.log(data);
            var image_box = document.getElementById("image_box");
            if (data.error) {
                document.getElementById("insufficent_credit_div").classList.remove("d-none");
                document.getElementById("inform_image_div").classList.add("d-none");
                document.getElementById("loading_img_div").classList.add("d-none");
                return; 
            }
            var imageData = data.images;

            localStorage.setItem('img_data', JSON.stringify(imageData));

            // Iterate over the 'content' array and create list items
            var index = 0;
            imageData.forEach(function(item) {
                var div = document.createElement('div');
                div.classList.add("col-md-4");
                div.classList.add("mb-4");

                html_content = '<div class="card">';
                html_content += '<div class="card-header">'+jsonData.content[index]["slide"]+'. '+jsonData.content[index]["heading"]+'</div>';
                html_content += '<div class="card-body p-0">';
                html_content += '<img src="'+item.image_path+'" class="img-fluid w-100 h-100" alt="Slide Image">';
                html_content += '</div>';
                html_content += '<div class="card-footer">';
                html_content += '<p  class="small">'+item.html_credit+'</p>';
                html_content += '</div>';
                html_content += '</div>';
                div.innerHTML = html_content;

                image_box.appendChild(div);
                index++;
            });

            document.getElementById("loading_img_div").classList.add("d-none");
            document.getElementById("success_image_div").classList.remove("d-none");
            document.getElementById("image_box_div").classList.remove("d-none");
            deduct_credit();

        })
        .catch(function(error) {
            console.error('Error [generateImages()]:', error);
        });
    }

    // Generate PPT Code
    function generatePPT() {
        var topic = topicInput.value;
        var raw_jsonData = localStorage.getItem('json_data');
        var raw_imgData = localStorage.getItem('img_data');
        var img_data = JSON.parse(raw_imgData);
    
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Set the appropriate Content-Type header
            },
            body: JSON.stringify({
                topic: topic,
                json_data: raw_jsonData,
                image_paths: img_data
            })
        })
        .then(function(response) {
            if (response.ok) {
                return response.json(); // Parse the JSON response from the server
            }
            throw new Error('Network response was not ok.');
        })
        .then(function(data) {
            if (data.error) {
                document.getElementById("insufficent_credit_div").classList.remove("d-none");
                document.getElementById("inform_image_div").classList.add("d-none");
                document.getElementById("loading_img_div").classList.add("d-none");
                return; 
            }

            // Check if the response contains the download link
            if (data && data.download_link) {
                // Create a link element
                var a = document.createElement('a');
                a.href = data.download_link;
                a.download = `${topic}_presentation.pptx`; // Set the download attribute with the desired file name
                a.click(); // Simulate a click event to download the file
                document.getElementById("success_div").classList.remove("d-none");
                deduct_credit();
            } else {
                console.error('Download link not found in the server response.');
            }

            document.getElementById("inform_ppt_div").classList.add("d-none");
            document.getElementById("loading_ppt_div").classList.add("d-none");
            
        })
        .catch(function(error) {
            console.error('Error [generatePPT()]:', error);
        });
    }
    
    // Deduct Credit 
    function deduct_credit() {
        var credit_count_element = document.getElementById("credit_count");
        if (credit_count_element != "Unlimited") {
            var credit_count = parseInt(credit_count_element.textContent); 
            credit_count = credit_count - 50;
            credit_count_element.textContent = credit_count;
        }
    }

});