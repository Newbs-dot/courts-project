import pymorphy3

# Create a morphological analyzer
morph = pymorphy3.MorphAnalyzer()

parsed_phrase = morph.parse('службы')
print(parsed_phrase)

# Print the results
for parse_result in parsed_phrase:
    print(parse_result.tag)