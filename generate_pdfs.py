import os
from fpdf import FPDF

# Markdown dosyasını oku
with open('academic_article.md', 'r', encoding='utf-8') as f:
    text = f.read()

class PDF(FPDF):
    def header(self):
        pass # Header'ı manuel ekleyeceğiz

    def footer(self):
        self.set_y(-15)
        # Arial italic 8 (standart font, TR karakterlerde sorun olabilir ama footer için risk alıyoruz veya düzelteceğiz)
        try:
            self.set_font('ArialCustom', '', 8)
        except:
             self.set_font('Arial', '', 8)
        self.cell(0, 10, 'Sayfa ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

pdf = FPDF()
pdf.alias_nb_pages()
pdf.add_page()

# Font ekleme - Windows için Arial
font_path = "C:\\Windows\\Fonts\\arial.ttf"
font_path_bold = "C:\\Windows\\Fonts\\arialbd.ttf"

try:
    if os.path.exists(font_path):
        # 'uni=True' is for old fpdf, new fpdf2 handles unicode automatically with TTF
        # We will try adding it without 'uni' first, if it fails we catch it.
        # But actually, best way is to just add it.
        pdf.add_font('ArialCustom', '', font_path, uni=True)
        pdf.add_font('ArialCustom', 'B', font_path_bold, uni=True)
        print("Arial fontu yüklendi.")
        main_font = 'ArialCustom'
    else:
        print("Arial fontu bulunamadı, standart font kullanılıyor (TR karakterler bozuk olabilir).")
        main_font = 'Arial'
except Exception as e:
    print(f"Font yükleme hatası: {e}")
    # Fallback
    main_font = 'Arial'

pdf.set_font(main_font, '', 11)

# Title
pdf.set_font(main_font, 'B', 16)
pdf.multi_cell(0, 10, 'Meta-Mühendislik Akademik Makale', 0, 'C')
pdf.ln(10)

lines = text.split('\n')
for line in lines:
    line = line.strip()
    if not line:
        pdf.ln(2)
        continue
    
    if line.startswith('# '):
        # Skip main title if processed or process as H1
        continue
    elif line.startswith('## '):
        # H2
        pdf.set_font(main_font, 'B', 14)
        pdf.cell(0, 10, line.replace('## ', ''), 0, 1)
        pdf.set_font(main_font, '', 11)
    elif line.startswith('**') and line.endswith('**') and len(line) < 100:
        # Subheading style
        pdf.set_font(main_font, 'B', 12)
        pdf.cell(0, 8, line.replace('**', ''), 0, 1)
        pdf.set_font(main_font, '', 11)
    elif line.startswith('**') and line.endswith('**'): 
        # Bold paragraph
        pdf.set_font(main_font, 'B', 11)
        pdf.multi_cell(0, 5, line.replace('**', ''))
        pdf.set_font(main_font, '', 11)
    else:
        # Normal text
        pdf.set_font(main_font, '', 11)
        clean_line = line.replace('**', '')
        pdf.multi_cell(0, 5, clean_line)

output_file = "Meta_Muhendislik_Makalesi_ResearchGate.pdf"
pdf.output(output_file)
print(f"PDF oluşturuldu: {output_file}")
