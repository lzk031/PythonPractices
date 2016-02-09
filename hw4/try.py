d = {'barney': set([]), 'dino': set([]), 'fred': set(['bam-bam', 'wilma', 'betty', 'barney']), 'betty': set([]), 'bam-bam': set([]), 'wilma': set(['dino', 'betty', 'fred'])}
a=d['fred'].copy
print a
print type(d['fred'])
#a.remove('bam-bam')