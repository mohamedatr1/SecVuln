from googletrans import Translator

def translator_dz(text):
    translator = Translator()
    
    try:
        # Translate from darija to English
        translation = translator.translate(text, dest='en')
        
        print(f"--- AI Analysis ---")
        print(f"Original (DZ): {text}")
        print(f"English Translation: {translation.text}")
        
        words = text.split()
        print(f"Complexity Score: {len(words)} tokens")
        
    except Exception as e:
        print(f"Error: {e}")


text = input("Enter Your Text to translate: ")
translator_dz(text)