# modify_gff_for_human_T2T
NCBIで公開されているT2T-CHM13v2.0のgffをsnpEffでのデータベース構築に向いた形に変更するプログラム

## Usage
```
usage: modify_gff.py [-h] -i I -o O

options:
  -h, --help        show this help message and exit
  -i I, --input I
  -o O, --output O
```

```
usage: modify_chrname.py [-h] [-f F] [-g G] [-t T] [-m M] [-of OF] [-og OG]
                         [-ot OT] [-bgzip BGZIP]

options:
  -h, --help            show this help message and exit
  -f F, --fasta F
  -g G, --gff G
  -t T, --tsv T
  -m M, --mode M
  -of OF, --out_fasta OF
  -og OG, --out_gff OG
  -ot OT, --out_txt OT
  -bgzip BGZIP, --bgzip BGZIP
```

## Detail

https://zenn.dev/anplat/articles/5ff90996e1cd45
