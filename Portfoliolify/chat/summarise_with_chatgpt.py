import json
from .extract_resume import extract_text_from_pdf
from .chat import model, client
from backend.utils.async_logging import async_log

def summarize_text(text):
    try:
        prompt = """
        Summarize the following content into the specified JSON format:
        {
            "personal": {
                "name": "Name",
                "email": "Email",
                "linkedin": "LinkedIn URL if it exists",
                "website": "URL link of personal website if it exists"
            },
            "summary": "Brief summary of the document",
            "education": "Brief summary of education",
            "skills": [
                "summary": "Brief summary of skills",
                "list": "All skills separated by ','",
            ],
            "experience": "List of internship or relevant experiences" [
                {
                    "title": "Title of internship 1"
                    "summary": "Summary of internship 1"
                },
                {
                    "title": "Title of internship 2"
                    "summary": "Summary of internship 2"
                }
            ],
            "project": "List of projects" [
                {
                    "title": "Title of project 1"
                    "summary": "Summary of project 1"
                },
                {
                    "title": "Title of project 2"
                    "summary": "Summary of project 2"
                }
            ]
        }

        Content:
        """ + text
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Please extract the following text into JSon format \n\n{prompt}"}
            ],
        )
        answer = response.choices[0].message.content.strip()
        async_log('Obtained summarised resume')
        return answer
    except Exception as e:
        async_log('Failed to summarise resume with ChatGPT', 'error')
        return 'error' + str(e)

def summarize_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    summary = summarize_text(text)
    summary = summary.replace('json', '')
    summary = summary.replace('```', '')
    json_summary = json.loads(summary)
    return json_summary

if __name__ == "__main__":
    pdf_path = 'path_to_your_pdf.pdf'
    summary = summarize_pdf(pdf_path)
    print(f"Summary:\n{summary}")
