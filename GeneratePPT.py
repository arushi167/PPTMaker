from PPTXModifier import PPTXModifier

class GeneratePPT:
    def __init__(self, output_filename, design_template):
        self.output_filename = output_filename
        self.design_template = design_template

    def start(self, image_list, json_data):
        replacements = []
        
        index = 1
        for data in json_data["content"]:
            heading = data["heading"]
            content = data["slidecontent"]
            text_dict = {'text': {}, 'images': {}}

            text_dict['slide'] = index
            text_dict['text'][f'heading{index}'] = heading
            text_dict['text'][f'content{index}'] = content

            text_dict['images'] = image_list[index-1]
            replacements.append(text_dict)
            index += 1

        ppt_modifier = PPTXModifier(self.design_template, self.output_filename, replacements)
        ppt_modifier.modify_pptx()
        return self.output_filename


if __name__ == "__main__":
    output_filename = "output.pptx"
    design_template = "static/template.pptx"
    test = GeneratePPT(output_filename, design_template)
    test.start()
