import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="https://gnomad.broadinstitute.org/api")
client = Client(transport=transport, fetch_schema_from_transport=True)

# For brevity, and to keep the focus on the Python code, we don't include every
# field from the raw query here.

query = gql(
    """
    query VariantsInGene {
      gene(gene_symbol: "BRCA1", reference_genome: GRCh38) {
        variants(dataset: gnomad_r4) {
          variant_id
          pos
          exome {
            ac
            ac_hemi
            ac_hom
            an
            af
          }
        }
      }
    }
"""
)

async def main():
    result = await client.execute_async(query)
    print(result)

if __name__ == "__main__":
    print("APSOKD call")
    asyncio.run(main())
    
