import argparse
import sys
from analyzer import fetch_crypto_data, analyze_data, export_to_csv

def main():
    parser = argparse.ArgumentParser(description="Crypto Market Analysis Tool")
    parser.add_argument(
        "--coin", 
        type=str, 
        default="bitcoin", 
        help="CoinGecko ID of the cryptocurrency (e.g., bitcoin, ethereum)"
    )
    parser.add_argument(
        "--days", 
        type=int, 
        default=365, 
        help="Number of days of historical data to fetch"
    )

    args = parser.parse_args()
    
    try:
        # 1. Fetch data
        df = fetch_crypto_data(args.coin, args.days)
        
        # 2. Analyze data
        analyzed_df = analyze_data(df)
        
        # 3. Export to CSV
        output_file = export_to_csv(analyzed_df, args.coin)
        
        print(f"Analysis complete. Results saved in {output_file}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
