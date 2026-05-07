def normalize_prompt_text(text):
    return (
        text.replace("Ã¢â‚¬â€œ", "-")
        .replace("Ã¢â‚¬â„¢", "'")
        .replace("Ã¢â‚¬Å“", '"')
        .replace("Ã¢â‚¬\u009d", '"')
    )


def clean_prompt_text(text):
    return (
        text.replace("\u00e2\u20ac\u201c", "-")  
        .replace("\u00e2\u20ac\u2122", "'")  
        .replace("\u00e2\u20ac\u0153", '"')  
        .replace("\u00e2\u20ac\u009d", '"')  
        .replace("\u0442\u0410\u0423", "-")  
        .replace("\u0442\u0410\u0429", "'")  
        .replace("\u0442\u0410\u042c", '"') 
        .replace("\u0442\u0410\u009d", '"') 
    )

