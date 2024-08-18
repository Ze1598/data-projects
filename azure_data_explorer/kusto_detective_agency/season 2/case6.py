text = """
{} {} {} {} {},
{} hidden {} {} {} {}.
{} {} {}, {} {} {} {}:
{} {} {}, {} {}.

{} rules {} {} {} {}:
{} {} {} {} {} {} {},
{} punctuations {} {} {},
{}'{} {} insensitive, {} {}.

{} {} {} {}, {}'{} {} {} {},
{} {} {} {} {} {} {}.
{} {} {}, {} {} {} {},
{} {} {} {} {} {} {}.

{} {} {} {} {} {} {}:
{} {} {} {} {} {} {} {}
{} {} {}, {} {} {} {},
{} {} {} {} - {} {} {} {}.

{} {} {} {}, {} {} {},
{} {} {} {} {}, {}'{} {}.
{}'{} {} {} {} {} {}
{} {}-{} {} {} {} {}.
"""

words = ["in","catalogue","of","titles","Grand","three","words","Demand","your","Hand","when","found","all","they","form","A","line","A","clear","timeline","simply","Fine","words","are","simple","to","Review","at","least","three","Letters","have","in","view","all","Mark","the","End","they","re","case","my","friend","to","find","all","words","you","ll","need","some","skill","seeking","the","popular","will","guide","you","still","below","The","King","the","first","word","mounts","the","Second","shares","with","Third","their","counts","reveal","the","last","word","with","Wise","thought","take","first","two","letters","from","word","most","sought","into","marked","dozen","and","change","just","one","and","with","those","two","the","word","is","done","so","search","the","titles","high","and","low","and","when","you","find","it","you","ll","know","you","ve","picked","the","Image","that","revealed","the","pass","code","to","the","World","concealed"]


for word in words:
    text = text.replace("{}", word, 1)

print(text.lower())