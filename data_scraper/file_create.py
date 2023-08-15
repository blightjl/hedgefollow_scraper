import html_pyppeteer

def main():
    next_name = html_pyppeteer.generate_source_name()
    html_pyppeteer.create_file(next_name)
    print("Created file with name: " + next_name)

if __name__ == "__main__":
    main()