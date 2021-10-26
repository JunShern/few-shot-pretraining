import argparse
import json
import pandas as pd
import streamlit as st
from pathlib import Path

class App:
    def __init__(self):
        st.set_page_config(page_title="Results Browser", page_icon=None, layout='wide')
        self.load_css("streamlit/style.css")
        return

    def load_css(self, css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        return

    @st.cache(suppress_st_warning=True, allow_output_mutation=True, max_entries=1)
    def get_file_names(self, data_dir: Path):
        st.warning("Cache miss: `get_trajectory_names` ran")
        file_paths = sorted([x for x in data_dir.glob("*/*.txt") if x.is_file()])
        file_names = [str(x) for x in file_paths]
        return file_names

    def run(self, data_dir):

        with st.sidebar:
            data_dir = Path(data_dir)
            st.write(f"Data dir: `{data_dir}`")

            # Load summary of data
            summary_csv = Path(data_dir / 'summary.csv')
            st.write(f"Summary file: `{summary_csv}`")
            if not summary_csv.exists():
                raise Exception(f"{summary_csv} does not exist!")
            full_df = pd.read_csv(summary_csv)
            df = full_df.select_dtypes(include=['bool'])
            counts = df.apply(pd.Series.value_counts).fillna(0)
            selected_criteria = st.radio(
                label="Select criteria:", 
                options=df.columns,
                format_func=lambda c: f"{c} ({int(counts[c].get(True))})")

            filtered_df = full_df[df[selected_criteria] == True]

            # Select file
            relevant_ids = list(filtered_df["doc_id"])
            chosen_id = st.selectbox(
                'Select a file:',
                relevant_ids)
            if chosen_id == None:
                return

        # Load metadata .json
        json_path = (Path(summary_csv).parent / "data" / str(chosen_id)).with_suffix(".json")
        try:
            with open(json_path, "r") as f:
                d = json.load(f)
        except FileNotFoundError:
            st.error(f"File {json_path} not found!")
            return

        # Main page content
        st.write(f"## `{chosen_id}`") 
        
        criteria = d['criteria']
        text = d['text']
        df = {
            'Criteria': [c for c in criteria],
            'Passed': [criteria[c]['passed'] for c in criteria],
            'Reason': [criteria[c]['reason'] for c in criteria],
            }
        df = pd.DataFrame(df)
        def highlight_true(s):
            if s.Passed == True:
                row_style = ['color: #ae81ff'] * len(s)
            else:
                row_style = [''] * len(s)
            return row_style
        st.write(df.style.apply(highlight_true, axis=1))
        
        if st.checkbox("Render text as Markdown", value=False):
            markdown_friendly_newlines = text.replace('\n', '  \n')
            st.markdown(markdown_friendly_newlines)
        else:
            st.text(text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize document results')
    parser.add_argument("-d", "--data-dir", default="./output",
                        help="Root directory containing document results. Default: %(default)s")
    options = parser.parse_args()

    app = App()
    app.run(options.data_dir)