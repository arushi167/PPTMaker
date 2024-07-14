import os
import zipfile
import tempfile
import shutil
import re

class PPTXModifier:
    def __init__(self, input_pptx, output_pptx, replacements):
        self.input_pptx = input_pptx
        self.output_pptx = output_pptx
        self.replacements = replacements

    def extract_pptx(self):
        temp_folder = tempfile.mkdtemp()
        with zipfile.ZipFile(self.input_pptx, 'r') as zip_ref:
            zip_ref.extractall(temp_folder)
        return temp_folder

    def update_slide_content(self, slide_xml_content, text_replacements, image_filename):
        # Update text in the slide
        for old_text, new_text in text_replacements.items():
            slide_xml_content = slide_xml_content.replace(old_text.encode(), new_text.encode())

        # Update image in the slide
        image_pattern = re.compile(rb'<a:blip .*? r:embed="(.*?)"', re.DOTALL)
        slide_xml_content = image_pattern.sub(f'<a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{image_filename}"'.encode(), slide_xml_content)

        return slide_xml_content

    def replace_images_in_media(self, temp_folder, image_paths):
        media_folder = os.path.join(temp_folder, 'ppt', 'media')
        for filename, image_path in image_paths.items():
            if image_path:
                shutil.copyfile(image_path, os.path.join(media_folder, filename))
                os.remove(image_path)

    def compress_to_pptx(self, temp_folder):
        with zipfile.ZipFile(self.output_pptx, 'w') as zip_ref:
            for foldername, subfolders, filenames in os.walk(temp_folder):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, temp_folder)
                    zip_ref.write(file_path, arcname)
        shutil.rmtree(temp_folder)

    def modify_pptx(self):
        temp_folder = self.extract_pptx()

        slides_in_template = len(os.listdir(os.path.join(temp_folder, 'ppt', 'slides'))) -1 
        output_ppt_length = len(self.replacements)
        extra_slides = output_ppt_length - slides_in_template
        print("Extra slides: ", extra_slides)

        slide_number = 1 
        if extra_slides > 0:
            for i in range(extra_slides):
                slide_xml_path = os.path.join(temp_folder, 'ppt', 'slides', f'slide{slide_number}.xml')
                des_xml_path = os.path.join(temp_folder, 'ppt', 'slides', f'slide{slide_number+slides_in_template}.xml')
                shutil.copy(slide_xml_path, des_xml_path)

                media_file = os.path.join(temp_folder, 'ppt', 'media', f'image{slide_number}.jpg')
                des_media_file = os.path.join(temp_folder, 'ppt', 'media', f'image{slide_number+slides_in_template}.jpg')
                shutil.copy(media_file, des_media_file)
                slide_number += 1
                
        elif extra_slides < 0:
            presentation_details = os.path.join(temp_folder, 'ppt', '_rels', 'presentation.xml.rels')
            with open(presentation_details, 'rb') as f:
                presentation_details_data = f.read()

            for i in range(abs(extra_slides)):
                slide_xml_path = os.path.join(temp_folder, 'ppt', 'slides', f'slide{output_ppt_length+slide_number}.xml')
                print(slide_xml_path)
                os.remove(slide_xml_path)

                slide_xml_path = os.path.join(temp_folder, 'ppt', 'slides', '_rels', f'slide{output_ppt_length+slide_number}.xml.rels')
                os.remove(slide_xml_path)
                print(slide_xml_path)

                presentation_details_data = presentation_details_data.replace(f'<Relationship Id="rId{output_ppt_length+slide_number+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{output_ppt_length+slide_number}.xml"/>'.encode(), ''.encode())

                media_file = os.path.join(temp_folder, 'ppt', 'media', f'image{output_ppt_length+slide_number}.jpg')
                os.remove(media_file)
                slide_number += 1

            with open(presentation_details, 'wb') as f:
                f.write(presentation_details_data)

        for replacement in self.replacements:
            slide_number = replacement['slide']
            text_replacements = replacement['text']
            image_filename = replacement['images']

            slide_xml_path = os.path.join(temp_folder, 'ppt', 'slides', f'slide{slide_number}.xml')
            with open(slide_xml_path, 'rb') as file:
                slide_xml_content = file.read()

            if image_filename:
                modified_slide_content = self.update_slide_content(slide_xml_content, text_replacements, image_filename.encode())
                with open(slide_xml_path, 'wb') as file:
                    file.write(modified_slide_content)

        # Replace images in the media folder
        image_paths = {}
        index = 1
        for replacement in self.replacements:
            image_paths[f'image{index}.jpg'] = replacement['images']
            index += 1
        self.replace_images_in_media(temp_folder, image_paths)

        self.compress_to_pptx(temp_folder)


if __name__ == "__main__":
    input_pptx = 'static/template.pptx'
    output_pptx = 'output.pptx'
    replacements = [
        {
            'slide': 1,
            'text': {
                'heading1': 'Updated Text 1',
                'content1': 'Updated Text 2'
            },
            'images': 'download1.jpg',
        },
        {
            'slide': 3,
            'text': {
                'heading3': 'Updated Text 1',
                'content3': 'Updated Text 2'
            },
            'images': 'download.jpg',
        }
    ]

    ppt_modifier = PPTXModifier(input_pptx, output_pptx, replacements)
    ppt_modifier.modify_pptx()

    print(f"Modified presentation saved to: {output_pptx}")

