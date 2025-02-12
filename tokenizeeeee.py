from whisper.tokenizer import get_tokenizer

def count_tokens(text):
    # Get the multilingual tokenizer
    tokenizer = get_tokenizer(multilingual=True)
    
    # Tokenize and count
    tokens = tokenizer.encode(text)
    
    print(f"Text: {text}")
    print(f"Number of tokens: {len(tokens)}")

# Example usage
if __name__ == "__main__":
    prompt = """El Monte tower with runways 1 and 19 on frequency 121.2. Traffic Alert, Cessna Three-Four Juliett, 12'o clock, 1 mile advise you turn left and climb immediately. """
    prompt += """ROOK01 climb and maintain flight level two zero zero. Report (advise) when formation join-up is complete"""
    prompt += """BAMA21 have BAMA23 squawk 5544, descend and maintain flight level one-niner-zero and change to my frequency"""
    prompt += """DMHS23 Radar contact (position if required). Cleared to SSC via direct. Descend and maintain flight level one-niner-zero."""
    prompt += """N5871S requesting flight break-up with N731K. N731K is changing destination to PHL."""

    count_tokens(prompt)


# this is only used to see how much prompt can be supplied
# inspiration: https://www.youtube.com/watch?v=PSKrr0sZJW0
# samples from here: https://www.faa.gov/air_traffic/publications/atpubs/atc_html/chap2_section_1.html
# whisper prompting: https://cookbook.openai.com/examples/whisper_prompting_guide