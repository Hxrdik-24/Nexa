import language_tool_python

tool = language_tool_python.LanguageTool("en-US")
def test():
    text = "I has a apple. He go to school everyday. She don't likes this."
    
    matches = tool.check(text)
    
    print("Original:")
    print(text)
    
    print("\nSuggestions:")
    
    for match in matches:
        print("Message:", match.message)
        print("Wrong:", text[match.offset:match.offset + match.error_length])
        print("Suggestions:", match.replacements[:5])
        print("-" * 40)
    
    corrected = language_tool_python.utils.correct(text, matches)
    
    print("\nCorrected:")
    print(corrected)
    
    tool.close()