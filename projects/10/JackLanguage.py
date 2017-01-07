#This file holds the Jack language so it can be used in our parser



class JackTokens:
#Keywords
    keywords = [
        "int",
        "char",
        "boolean",
        "method",
        "function",
        "constructor",
        "void",
        "var",
        "static",
        "filed",
        "let",
        "do",
        "if",
        "else",
        "while",
        "return",
        "true",
        "false",
        "null",
        "this",
        "class",
    ]
#Symbols
    symbols = [
        "{","}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~", "\\"
    ]
#We also have integerConstant, StringConstant and identifier, which cannot be encapsulated in a list, so
# TODO: find a way to workaround this not too complicated issue
