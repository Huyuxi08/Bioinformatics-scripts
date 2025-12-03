# -*- coding: utf-8 -*-
###Keep gene features from the gene list
import sys
import os
import gffutils

gff_file = sys.argv[1]
Gene_list = sys.argv[2]
out_file = sys.argv[3]

dbname = os.path.basename(gff_file) + ".db"

if os.path.exists(dbname):
    db = gffutils.FeatureDB(dbname, keep_order=True)
else:
    db = gffutils.create_db(gff_file, dbfn=dbname, force=True, keep_order=True, merge_strategy='merge')

with open(Gene_list, "r") as f:
    keep_ids = [line.strip() for line in f if line.strip()]

with open(out_file, 'w') as out:
    out.write("##gff-version 3\n")
    for gid in keep_ids:
        try:
            gene = db[gid]
        except gffutils.FeatureNotFoundError:
            print(f"[Warning] ID not found in GFF: {gid}", file=sys.stderr)
            continue

        out.write(str(gene) + '\n')
        for feature in db.children(gene, level=None, order_by=('seqid', 'start')):
            out.write(str(feature) + '\n')
