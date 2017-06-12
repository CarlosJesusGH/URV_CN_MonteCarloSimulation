import os
import utils_files


def build_latex(input_dir, output_path):
    utils_files.remove_file_dir(output_path)
    for subdir, dirs, files in os.walk(input_dir):
        last_subdir = ""
        for file in sorted(files):
            if "terminal_logs" not in subdir:   # not include this sub directory
                if subdir != last_subdir:
                    # Add new section to latex
                    subdir_name = subdir[subdir.rfind("/") + 1:]
                    print(subdir_name)
                    add_new_section(subdir_name)
                    last_subdir = subdir

                print("    " + file.replace("\n", " - "))



def add_image(image_path, caption="", label=""):
    file = create_or_open_file()

    image_template = '\t\\begin{figure}[H]\n' \
                     '\t\t\centering\n' \
                     '\t\t\includegraphics[width=1 \\textwidth]{\"/home/cj/Dropbox/Personal/Study/MasterURV/2nd Semester/' \
                     'CN/Activity 1' + image_path.replace('..', '').replace('.png','') + '\"}\n' \
                     '\t\t\caption{' + caption + '}\n' \
                     '\t\t\label{' + label + '}\n' \
                     '\t\end{figure}'
    file.write(image_template + "\n\n")
    file.close()

def create_or_open_file():
    if not os.path.exists(latex_output_path):
        file = open(latex_output_path, 'w+')
        file.write("ini\n")
    else:
        file = open(latex_output_path, 'a')
    return file

def add_new_page():
    file = create_or_open_file()
    file.write("\n\n%-------------------------------------------------------\n"
               "\\newpage\n")
    file.close()


def add_simple_text(text=""):
    file = create_or_open_file()
    file.write(text.replace('_','\\_'))
    file.close()


def add_new_section(title):
    add_simple_text("\\section{" + title + "}\n\n")


def add_new_subsection(title):
    add_simple_text("\\subsection{" + title + "}\n\n")

latex_input_dir = "../../output_complete"
latex_output_path = "../../report/latex/report_helper.tex"
build_latex(latex_input_dir, latex_output_path)