import argparse
import gzip
import sys


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='i', type=str, required=True)
    parser.add_argument('-o', '--output', dest='o', type=str, required=True)
    args = parser.parse_args()
    return args


class modify_gff:
    def read_write_gff(self, args):
        write_per = 1000
        if args.i.endswith('.gz'):
            igff = gzip.open(args.i, mode='rt')
        else:
            igff = open(args.i, mode='rt')
        ogff = open(args.o, mode='w')
        line = igff.readline()
        headers = []
        self.tmp_lines_gff = []
        self.ovnum = 0
        while line:
            if line.startswith('#'):
                headers.append(line.strip())
                line = igff.readline()
                continue
            elif self.ovnum == 0:
                print('\n'.join(headers))
                ogff.write('\n'.join(headers))
            self.ovnum += 1
            data = line.strip().split(sep='\t')
            if data[2] == 'gene':
                self.gene_name = (data[8].strip().split(';'))[0]
                self.gene_name = self.gene_name[8:]
                self.tmp_lines_gff.append('\t'.join(data))
            elif data[2] == "pseudogene":
                self.modify_pseudo_gene(data)
                self.ovnum += 1
            elif data[2] == "miRNA":
                self.modify_mirna(data)
            elif data[2] == "lnc_RNA":
                data[2] = "ncrna"
                self.tmp_lines_gff.append('\t'.join(data))
            elif data[2] == "primary_transcript":
                data[2] = "transcript"
                print(self.ovnum)
                self.tmp_lines_gff.append('\t'.join(data))
            elif data[1] == 'RefSeqFE':
                self.modify_refseqFE(data)
            else:
                self.tmp_lines_gff.append('\t'.join(data))
            line = igff.readline()
            if self.ovnum % write_per == 0:
                outtxt_gff = '\n' + '\n'.join(self.tmp_lines_gff)
                print(f'{self.ovnum} done')
                ogff.write(outtxt_gff)
                self.tmp_lines_gff = []
            if len(line) > 0:
                continue
        outtxt_gff = '\n' + '\n'.join(self.tmp_lines_gff)
        outtxt_gff
        ogff.write(outtxt_gff)
        igff.close()
        ogff.close()

    def modify_pseudo_gene(self, data):
        data[2] = "gene"
        self.tmp_lines_gff.append('\t'.join(data))
        p_attributes = data[8].strip().split(';')
        if p_attributes[0].startswith("ID=gene-"):
            pgene_name = p_attributes[0][8:]
        elif p_attributes[0].startswith("ID=pseudogene-"):
            pgene_name = p_attributes[0][14:]
        self.gene_name = pgene_name
        p_attributes[0] = "ID=pseudogene-" + pgene_name
        p_attributes.insert(1, f"Parent=gene-{pgene_name}")
        data[8] = ';'.join(p_attributes)
        data[2] = "pseudogene"
        self.tmp_lines_gff.append('\t'.join(data))

    def modify_mirna(self, data):
        mir_attributes = data[8].strip().split(';')
        mir_attributes[1] = f"Parent=gene-{self.gene_name}"
        data[8] = ';'.join(mir_attributes)
        self.tmp_lines_gff.append('\t'.join(data))

    def modify_refseqFE(self, data):
        if data[2] == "biological_region":
            pass
        else:
            data[2] = "inter_cns"
            self.tmp_lines_gff.append('\t'.join(data))

    def run(self, args):
        self.read_write_gff(args)


def main():
    args = argument_parser()
    mgff = modify_gff()
    mgff.run(args)
    sys.exit(0)


if __name__ == '__main__':
    main()
