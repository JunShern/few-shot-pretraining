import argparse
import json
import pandas as pd
import streamlit as st
from pathlib import Path

class App:
    def __init__(self):
        st.set_page_config(page_title="Results Browser", page_icon=None, layout='wide')
        self.load_css("style.css")
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

            # Select CSV
            csv_names = sorted([str(x) for x in data_dir.glob("*/*.csv") if x.is_file()])
            selected_csv = st.sidebar.selectbox(
                'Select a csv:',
                csv_names)
            if selected_csv is None:
                return
            
            full_df = pd.read_csv(selected_csv)
            df = full_df.select_dtypes(include=['bool'])
            counts = df.apply(pd.Series.value_counts).fillna(0)
            selected_criteria = st.radio(
                label="Select criteria:", 
                options=df.columns,
                format_func=lambda c: f"{c} ({int(counts[c].get(True))})")

            filtered_df = full_df[df[selected_criteria] == True]

            # Select file
            relevant_ids = list(filtered_df["doc_id"])
            file_names = [(Path(selected_csv).parent / str(doc_id)).with_suffix(".txt") for doc_id in relevant_ids]
            chosen_path = st.selectbox(
                'Select a file:',
                file_names)
            if chosen_path == None:
                return

        try:
            with open(chosen_path, "r") as f:
                d = json.load(f)
        except FileNotFoundError:
            st.error(f"File {chosen_path} not found!")
            return

        st.write(f"## `{chosen_path}`") 
        criteria = d['criteria']
        df = {
            'Criteria': [c['criterion'] for c in criteria],
            'Passed': [c['passed'] for c in criteria],
            'Reason': [c['reason'] for c in criteria],
            }
        df = pd.DataFrame(df)
        def highlight_true(s):
            if s.Passed == True:
                row_style = ['color: #ae81ff'] * len(s)
                # row_style = ['background-color: #245263'] * len(s)
            else:
                row_style = [''] * len(s)
            return row_style
        st.write(df.style.apply(highlight_true, axis=1))
        
        if st.checkbox("Render text as Markdown", value=False):
            markdown_friendly_newlines = d['text'].replace('\n', '  \n')
            st.markdown(markdown_friendly_newlines)
        else:
            st.text(d['text'])
        with st.expander("Full JSON", expanded=False):
            st.write(d)
        # st.balloons()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize document results')
    parser.add_argument("-d", "--data-dir", default="./output",
                        help="Root directory containing document results. Default: %(default)s")
    options = parser.parse_args()

    app = App()
    app.run(options.data_dir)