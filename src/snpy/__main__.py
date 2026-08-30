import json
import requests

from .eqtl import get_variant, get_eqtl
import polars as pl
import argparse

"""
parser = argparse.ArgumentParser(description="Compute EFO/HPO embedding similarity")

# positional argument (required, no dashes)


parser.add_argument("--input_file", help="Path to input TSV")

# optional flag with a value
parser.add_argument("--model", default="anacletix", choices=["sapbert", "biolord"],
                     help="Which embedding model to use")

# numeric argument
parser.add_argument("--top-k", type=int, default=10,
                     help="Number of nearest neighbors to return")

# argument accepting multiple values
parser.add_argument("--tissues", nargs="+", default=None,
                     help="One or more GTEx tissue names")

args = parser.parse_args()
print(args.input_file)
print(args.model)
print(args.top_k)
print(args.tissues)
"""

with open("test/data/best_snps.txt","r") as f:
    snps = [line.strip() for line in f]

 
#snps = ['rs12938','rs983751','rs983751']
#variants = ['chr10_88986936_A_C_b38']

print(snps)

if __name__ == "__main__":   
    data = get_eqtl(snps)
    df = pl.DataFrame(data)
    print(df)
    df.write_csv("test/output/best_snps.csv")

