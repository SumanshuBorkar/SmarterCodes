import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import logging
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from app.config import settings

logger = logging.getLogger(__name__)


class HTMLProcessor:
    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def fetch_html_content(self, url: str) -> str:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch URL {url}: {e}")
            raise

    def clean_html(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, "html.parser")

        for element in soup(
            [
                "script",
                "style",
                "meta",
                "link",
                "nav",
                "footer",
                "header",
                "aside",
                "form",
                "button",
                "iframe",
                "noscript",
            ]
        ):
            element.decompose()

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

        text = soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)

        text = re.sub(
            r"\n\s*\n", "\n\n", text
        ) 
        text = re.sub(
            r"[ \t]+", " ", text
        )

        return text

    def split_into_chunks(self, text: str, max_tokens: int = None) -> List[str]:
        if max_tokens is None:
            max_tokens = settings.MAX_TOKENS_PER_CHUNK

        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_count = 0

        for paragraph in paragraphs:
            if not paragraph.strip():
                continue

            words = paragraph.split()
            paragraph_tokens = len(words) * 1.3

            if paragraph_tokens > max_tokens:
                sentences = re.split(r"(?<=[.!?])\s+", paragraph)
                for sentence in sentences:
                    if not sentence.strip():
                        continue
                    words = sentence.split()
                    sentence_tokens = len(words) * 1.3

                    if current_count + sentence_tokens > max_tokens and current_chunk:
                        chunks.append(" ".join(current_chunk))
                        current_chunk = [sentence]
                        current_count = sentence_tokens
                    else:
                        current_chunk.append(sentence)
                        current_count += sentence_tokens
            else:
                if current_count + paragraph_tokens > max_tokens and current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [paragraph]
                    current_count = paragraph_tokens
                else:
                    current_chunk.append(paragraph)
                    current_count += paragraph_tokens

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.embedding_model.encode(texts)
        return embeddings.tolist()

    def process_url(self, url: str) -> Tuple[List[str], List[List[float]]]:
        html_content = self.fetch_html_content(url)
        clean_text = self.clean_html(html_content)

        chunks = self.split_into_chunks(clean_text)

        embeddings = self.generate_embeddings(chunks)

        return chunks, embeddings


html_processor = HTMLProcessor()
