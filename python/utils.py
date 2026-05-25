def apply_theme(widget, bg="#f0f0f0", fg="#000000"):
    widget.configure(bg=bg)
    for child in widget.winfo_children():
        # Recursively apply background
        try:
            child.configure(bg=bg, fg=fg)
        except:
            pass
        if child.winfo_children():
            apply_theme(child, bg, fg)
