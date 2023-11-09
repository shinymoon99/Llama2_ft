import re

def c2DueeFormatFromSL(input, source_text, label2role):
    # Example usage:
# input_text = "{点选}<t>点击</t><o>“文件”</o>，<i>打开文件菜单</i>。"
# source_text = "点击“文件”，打开文件菜单。"
# label2role = {"t": "trigger", "o": "object", "i": "impact"}

# output = c2DueeFormatFromSL(input_text, source_text, label2role)
# print(output)
    result = {
        "text": source_text,
        "id": 1,
        "event_list": []
    }

    etype_pattern = r'{(.*?)}'
    arg_pattern = r'<(.*?)>(.*?)</\1>'

    event_matches = re.finditer(etype_pattern, input)
    
    for i, event_match in enumerate(event_matches):
        event_type = event_match.group(1)
        event_start = event_match.start()
        
        event = {
            "event_type": event_type,
            "trigger": "",
            "trigger_start_index": event_start,
            "arguments": []
        }
        
        arg_matches = re.finditer(arg_pattern, event_match.group(0))
        
        for arg_match in arg_matches:
            tag = arg_match.group(1)
            arg_text = arg_match.group(2)
            arg_start = arg_match.start()
            arg_end = arg_match.end()
            role = label2role.get(tag, "")
            
            argument = {
                "argument_start_index": arg_start,
                "argument_end_index": arg_end,
                "role": role,
                "argument": arg_text,
                "alias": []
            }
            
            event["arguments"].append(argument)
        
        result["event_list"].append(event)
    
    return result


