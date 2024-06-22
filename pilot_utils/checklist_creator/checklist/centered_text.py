class CenteredText:
    def __init__(self,
                 text: str,
                 is_bold: bool
                 ):
        """
            Class that represents a centered line in the checklist

        Params
        ------
            text (str):
                Text that should be displayed
            is_bold (bool):
                Whether the text should be displayed in bold.
        """
        self.text = text
        self.is_bold = is_bold
