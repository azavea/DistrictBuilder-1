package main

import (
	"bufio"
	"encoding/csv"
	"io"
	"log"
	"os"
	"strings"
	"golang.org/x/net/html"
)

func main() {
	csvFilePath := os.Args[1]
	if csvFilePath == "" {
		log.Fatal("No CSV file path specified.")
	}
	htmlFilePath := os.Args[2]
	if htmlFilePath == "" {
		log.Fatal("No HTML directory path specified.")
	}
	
	lines, err := GetLines(csvFilePath)
	if err != nil {
		log.Fatal(err)
	}

	var missingFiles []string
	var newLines [][]string
	for i, line := range lines {
		if i == 0 {
			newLine := append(line, "competitiveness", "split_counties", "majority_minority", "compactness", "population_equivalence")
			newLines = append(newLines, newLine)
			continue
		}
		id := line[0]
		file, err := os.Open(htmlFilePath + id + ".html")
		if err != nil {
			missingFiles = append(missingFiles, id)
			continue
		}
		data := ReadHTML(bufio.NewReader(file))
		newLine := append(line, data...)
		newLines = append(newLines, newLine)
	}

	log.Println("Missing Files:", missingFiles)

	WriteCSV(newLines);
}

func GetLines(filePath string) ([][]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}

	r := csv.NewReader(bufio.NewReader(file))
	var lines [][]string
	for {
		record, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		lines = append(lines, record)
	}
	return lines, nil
}

func ReadHTML(r io.Reader) []string {
	var data []string
	z := html.NewTokenizer(r)

	for {
		tt := z.Next()

		// If it's an error or the end, break out
		if tt == html.ErrorToken {
			break
		}
		// if it's not a start token, continue
		if tt != html.StartTagToken {
			continue
		}

		t := z.Token()

		// if it's not a div or it has no attributes like "class", continue
		if t.Data != "div" || len(t.Attr) == 0 {
			continue
		}
		// if the class isn't "plan_summary congressional", continue
		if t.Attr[0].Val != "plan_summary congressional" {
			continue
		}

		// Now we have the correct div, so we dig until we get all the data we need
		for len(data) != 5 {
			tt2 := z.Next()

			// If we aren't at a "label" start tag, continue
			if tt2 != html.StartTagToken || z.Token().Data != "label" {
				continue
			}

			// We are at a start label tag

			// Get the content of the label tag
			z.Next()
			label := z.Token().Data

			// If it's one of the pieces of data we want, keep going
			if label == "Competitiveness" || label == "Split Counties" || label == "Majority-Minority" || label == "Compactness" || label == "Population Equivalence" {
				z.Next() // label end tag
				z.Next() // span start tag
				z.Next() // this should be the value

				// Add the value; if it has " (of 18)", remove
				data = append(data, strings.Replace(z.Token().Data, " (of 18)", "", 1))
			}
		}
	}

	return data
}

func WriteCSV(lines [][]string) {
	fo, err := os.Create("output.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer func() {
        if err := fo.Close(); err != nil {
            panic(err)
        }
    }()
    w := csv.NewWriter(bufio.NewWriter(fo))

	for _, record := range lines {
		if err := w.Write(record); err != nil {
			log.Fatalln("error writing record to csv:", err)
		}
	}

	w.Flush()

	if err := w.Error(); err != nil {
		log.Fatal(err)
	}
}
