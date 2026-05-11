# ── DPI-fix til Windows (skal stå ALLERØVERST inden tk importeres) ────────────
import ctypes, sys
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)   # Per-monitor DPI v2
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from PIL import Image, ImageTk, ImageOps
import os, json, pathlib

# ─────────────────────────────────────────────────────────────────────────────
#  KONFIGURATION  –  tilpas disse stier til din mappestruktur
# ─────────────────────────────────────────────────────────────────────────────
DATA_FILE  = r"C:\GitHub\Innovativ app\Rådne kammerjunker\Data\ratings.json"
IMAGE_DIR  = r"C:\GitHub\Innovativ app\Rådne kammerjunker\Images"
#
#  Læg billederne i IMAGE_DIR og navngiv dem præcis som "image" nedenfor,
#  f.eks.:  klover_citron.jpg   (PNG og JPG understøttes begge)
#  Hvis der ikke er et billede til en vare, vises en pæn pladsholder.
# ─────────────────────────────────────────────────────────────────────────────

KOLDSKÅL = [
    {
        "name":        "Kløver koldskål med citron",
        "brand":       "Kløver",
        "image":       "klover_citron",          # filnavn uden extension
        "description": "En frisk og let koldskål med naturlig citronaroma. "
                        "Perfekt balanceret syre og sødme — ideel til de varmeste sommerdage. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 256 kJ / 60 kcal \n"
                        "Fedt: 0,5 gram \n"
                        "Heraf mættede fedtsyrer: 0,3 gram \n"
                        "Kulhydrater: 11 gram \n"
                        "Heraf sukkerarter: 10 gram \n"
                        "Protein: 3 gram \n"
                        "Salt: 0,1 gram \n",
    },
    {
        "name":        "Kløver koldskål med tykmælk og æg",
        "brand":       "Kløver",
        "image":       "klover_tykmælk",
        "description": "Den klassiske opskrift med tykmælk og æg giver en fyldig og cremet "
                        "konsistens. En trofast følgesvend til sprøde kammerjunkere. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 286 kJ / 68 kcal \n"
                        "Fedt: 2,1 gram \n"
                        "Heraf mættede fedtsyrer: 1,3 gram \n"
                        "Kulhydrater: 8,1 gram \n"
                        "Heraf sukkerarter: 8,1 gram \n"
                        "Protein: 3,5 gram \n"
                        "Salt: 0,11 gram \n",
    },
    {
        "name":        "Mejse koldskål",
        "brand":       "Mejse",
        "image":       "mejse",
        "description": "Mejses bud på den danske sommertradition. En mild og delikat smag med "
                        "en fin cremet tekstur, der appellerer til hele familien. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 288 kJ / 69 kcal \n"
                        "Fedt: 2,2 gram \n"
                        "Heraf mættede fedtsyrer: 1,3 gram \n"
                        "Kulhydrater: 8,1 gram \n"
                        "Heraf sukkerarter: 8,1 gram \n"
                        "Protein: 3,5 gram \n"
                        "Salt: 0,1 gram \n",
    },
    {
        "name":        "Løgismose mormor koldskål",
        "brand":       "Løgismose",
        "image":       "logismose_mormor",
        "description": "Lavet efter bedstemors originale opskrift med kærlighed og omhu. "
                        "Autentisk smag der tager dig tilbage til barndommens somre. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 321 kJ / 77 kcal \n"
                        "Fedt: 2,2 gram \n"
                        "Heraf mættede fedtsyrer: 1,4 gram \n"
                        "Kulhydrater: 11 gram \n"
                        "Heraf sukkerarter: 11 gram \n"
                        "Protein: 3,1 gram \n"
                        "Salt: 0,09 gram \n",
    },
    {
        "name":        "Løgismose farmor koldskål",
        "brand":       "Løgismose",
        "image":       "logismose_farmor",
        "description": "Lavet efter farmors originale opskrift med kærlighed og omhu. "
                        "Autentisk smag der tager dig tilbage til barndommens somre. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 239 kJ / 56 kcal \n"
                        "Fedt: 0,8 gram \n"
                        "Heraf mættede fedtsyrer: 0,5 gram \n"
                        "Kulhydrater: 9,2 gram \n"
                        "Heraf sukkerarter: 7,9 gram \n"
                        "Protein: 3,1 gram \n"
                        "Salt: 0,1 gram \n",
    },
    {
        "name":        "Måms koldskål",
        "brand":       "Måms",
        "image":       "maams",
        "description": "En blød og rund koldskål med en dejlig naturlig sødme. Populær "
                        "blandt børn og voksne der sætter pris på en mild smag. \n \n"
                        "Ukendt ernæringsindhold\n",
    },
    {
        "name":        "Salling koldskål",
        "brand":       "Salling",
        "image":       "salling",
        "description": "Sallings eget mærke tilbyder en solid koldskål til en fornuftig pris. "
                        "God hverdagskoldskål med en klassisk og velkendt smag. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 282 kJ / 67 kcal \n"
                        "Fedt: 0,9 gram \n"
                        "Heraf mættede fedtsyrer: 0,5 gram \n"
                        "Kulhydrater: 12 gram \n"
                        "Heraf sukkerarter: 11 gram \n"
                        "Protein: 3 gram \n"
                        "Salt: 0,1 gram \n",
    },
    {
        "name":        "Salling øko koldskål",
        "brand":       "Salling",
        "image":       "salling_oko",
        "description": "Den økologiske udgave fra Salling. Samme gode smag, produceret med "
                        "respekt for naturen og certificerede råvarer. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 313 kJ / 75 kcal \n"
                        "Fedt: 2,2 gram \n"
                        "Heraf mættede fedtsyrer: 1,4 gram \n"
                        "Kulhydrater: 11 gram \n"
                        "Heraf sukkerarter: 11 gram \n"
                        "Protein: 3,2 gram \n"
                        "Salt: 0,1 gram \n",
    },
    {
        "name":        "Thiese koldskål",
        "brand":       "Thiese",
        "image":       "thiese",
        "description": "Fra det anerkendte mejeri Thiese — en delikat koldskål med "
                        "karakterfuld og frisk smag. Et premium valg til de kræsne. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 334 kJ / 73 kcal \n"
                        "Fedt: 2 gram \n"
                        "Heraf mættede fedtsyrer: 1,2 gram \n"
                        "Kulhydrater: 12 gram \n"
                        "Heraf sukkerarter: 12 gram \n"
                        "Protein: 3,3 gram \n"
                        "Salt: 0,17 gram \n",
    },
    {
        "name":        "Thiese laktosefri koldskål",
        "brand":       "Thiese",
        "image":       "thiese_laktosefri",
        "description": "Alle kan nu nyde koldskålsoplevelsen med Thieses laktosefri variant. "
                        "Samme cremede smag — ingen bekymringer. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 247 kJ / 58 kcal \n"
                        "Fedt: 0,7 gram \n"
                        "Heraf mættede fedtsyrer: 0,3 gram \n"
                        "Kulhydrater: 9,7 gram \n"
                        "Heraf sukkerarter: 9,7 gram \n"
                        "Protein: 3,3 gram \n"
                        "Salt: 0,1 gram \n",
    },
    {
        "name":        "Naturmælk koldskål",
        "brand":       "Naturmælk",
        "image":       "naturmaelk",
        "description": "Produceret af køer der græsser frit på naturens marker. En ren og "
                        "frisk smag der afspejler det gode danske landbrug. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 311 kJ / 74 kcal \n"
                        "Fedt: 2,1 gram \n"
                        "Heraf mættede fedtsyrer: 1,3 gram \n"
                        "Kulhydrater: 11 gram \n"
                        "Heraf sukkerarter: 11 gram \n"
                        "Protein: 3,1 gram \n"
                        "Salt: 0,1 gram \n",
    },
    {
        "name":        "Øllingegård koldskål",
        "brand":       "Øllingegård",
        "image":       "ollingegaard",
        "description": "Fra det lille Øllingegård mejeri, drevet med passion og håndværk. "
                        "En håndlavet koldskål med dybde og karakter. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 311 kJ / 74 kcal \n"
                        "Fedt: 2,1 gram \n"
                        "Heraf mættede fedtsyrer: 1,3 gram \n"
                        "Kulhydrater: 11 gram \n"
                        "Heraf sukkerarter: 11 gram \n"
                        "Protein: 3,1 gram \n"
                        "Salt: 0,1 gram \n",
    },
    {
        "name":        "Arla original koldskål",
        "brand":       "Arla",
        "image":       "arla_original",
        "description": "Arlas klassiker der har vundet danskernes hjerter i generationer. "
                        "En pålidelig og velsmagende koldskål til sommerbordet. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 296 kJ / 70 kcal \n"
                        "Fedt: 2 gram \n"
                        "Heraf mættede fedtsyrer: 1,2 gram \n"
                        "Kulhydrater: 8,7 gram \n"
                        "Heraf sukkerarter: 8,7 gram \n"
                        "Protein: 3,5 gram \n"
                        "Salt: 0,11 gram \n",
    },
    {
        "name":        "Arla koldskål med jordbær",
        "brand":       "Arla",
        "image":       "arla_jordbær",
        "description": "En sommerlig twist på klassikeren med søde, modne jordbær. "
                        "Perfekt til dem der ønsker lidt ekstra frugtighed. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 271 kJ / 64 kcal \n"
                        "Fedt: 1,7 gram \n"
                        "Heraf mættede fedtsyrer: 1,1 gram \n"
                        "Kulhydrater: 8,4 gram \n"
                        "Heraf sukkerarter: 8 gram \n"
                        "Protein: 3,1 gram \n"
                        "Salt: 0,1 gram \n",
    },
    {
        "name":        "Cheasy koldskål",
        "brand":       "Cheasy",
        "image":       "cheasy",
        "description": "En spændende variant fra Cheasy med en let og luftig konsistens. "
                        "Mild og frisk med et strejf af kreativitet. \n \n"
                        "Ernæringsindhold pr. 100 ml:\n"
                        "Energi: 177 kJ / 42 kcal \n"
                        "Fedt: 1,2 gram \n"
                        "Heraf mættede fedtsyrer: 0,8 gram \n"
                        "Kulhydrater: 3,7 gram \n"
                        "Heraf sukkerarter: 3,5 gram \n"
                        "Protein: 3,4 gram \n"
                        "Salt: 0,1 gram \n",
    },
]

# ── Farvepalette – komplementerer #fdfddb ────────────────────────────────────
BG        = "#fdfddb"   # varm citrongul baggrund
CARD      = "#ffffff"   # rene hvide kort
BORDER    = "#e8e4b8"   # dæmpet guld-beige kant
BORDER_HV = "#b5a84a"   # kant ved hover
NAV_BG    = "#2b2b1e"   # mørk oliven nav-bar
NAV_FG    = "#fdfddb"   # navtekst = baggrundsfarven
TEXT      = "#1a1a0e"   # næsten sort tekst
TEXT_SUB  = "#6b6440"   # olivenbrun sekundær tekst
ACCENT    = "#4a7c59"   # grøn CTA (komplementær til gul)
ACCENT_H  = "#3a6147"   # mørkere grøn hover
SCORE_CLR = "#b07d00"   # mørk guld til score-tal
BAR_BG    = "#e8e4b8"   # progress-bar baggrund
BAR_FG    = "#4a7c59"   # progress-bar fyld

# ── Billede-hjælper ───────────────────────────────────────────────────────────
_img_cache: dict = {}

def load_image(image_key: str, w: int, h: int) -> "ImageTk.PhotoImage | None":
    cache_key = f"{image_key}_{w}_{h}"
    if cache_key in _img_cache:
        return _img_cache[cache_key]

    base = pathlib.Path(IMAGE_DIR)
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".bmp"):
        path = base / f"{image_key}{ext}"
        if path.exists():
            try:
                img = Image.open(path).convert("RGB")
                img.thumbnail((w, h), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                _img_cache[cache_key] = photo
                return photo
            except Exception:
                break
    return None   # Ingen billede fundet


def placeholder(w: int, h: int, bg: str = BORDER) -> "ImageTk.PhotoImage":
    """Simpel ensfarvet pladsholder-billede."""
    cache_key = f"__ph_{w}_{h}_{bg}"
    if cache_key in _img_cache:
        return _img_cache[cache_key]
    img = Image.new("RGB", (w, h), bg)
    photo = ImageTk.PhotoImage(img)
    _img_cache[cache_key] = photo
    return photo


# ── Data helpers ──────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({k["name"]: [] for k in KOLDSKÅL}, f, indent=4, ensure_ascii=False)

def load_ratings():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_rating(name, value):
    data = load_ratings()
    data.setdefault(name, []).append(value)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_avg(data, name):
    r = data.get(name, [])
    return (sum(r) / len(r), len(r)) if r else (None, 0)


# ── App ───────────────────────────────────────────────────────────────────────
class KoldskålApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Rådne Kammerjunker")
        self.root.geometry("1920x1080")
        self.root.minsize(1600, 900)
        self.root.configure(bg=BG)

        # Skalér fonte op – løser grynetheden på høj-DPI
        self._F = self._make_font_factory()
        self.fn  = self._F(11)
        self.fn_b = self._F(11, "bold")
        self.fs   = self._F(10)
        self.fxs  = self._F(9)
        self.fh1  = self._F(20, "bold")
        self.fh2  = self._F(13, "bold")
        self.fh3  = self._F(11, "bold")
        self.fnum = self._F(40, "bold")
        self.fnav = self._F(13, "bold")

        self._build_shell()
        self._show_browse()

    # ── Font factory: finder bedste sans-serif font ──────────────────────────
    @staticmethod
    def _make_font_factory():
        preferred = ["Segoe UI", "Helvetica Neue", "Arial", "Liberation Sans"]
        chosen = "TkDefaultFont"
        for fam in preferred:
            try:
                f = tkfont.Font(family=fam, size=12)
                if fam.lower() in f.actual("family").lower():
                    chosen = fam
                    break
            except Exception:
                pass
        def F(size, weight="normal"):
            return tkfont.Font(family=chosen, size=size, weight=weight)
        return F

    # ── Shell ─────────────────────────────────────────────────────────────────
    def _build_shell(self):
        nav = tk.Frame(self.root, bg=NAV_BG, height=56)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        tk.Label(nav, text="Rådne Kammerjunker", bg=NAV_BG, fg=NAV_FG,
                 font=self.fnav, padx=28).pack(side="left", fill="y")
        tk.Label(nav, text="Koldskål guide",
                 bg=NAV_BG, fg="#888870", font=self.fxs, padx=4).pack(side="left", fill="y")
        tk.Label(nav, text="🥛", bg=NAV_BG, fg=NAV_FG, font=tkfont.Font(size=22),
                 padx=28).pack(side="right", fill="y")

        # 2 px separator i accentfarve
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill="x")

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(fill="both", expand=True)

    def _clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ── Scroll-canvas ─────────────────────────────────────────────────────────
    def _scrollable(self, parent) -> tk.Frame:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TScrollbar",
                        troughcolor=BG, background=BORDER,
                        darkcolor=BORDER, lightcolor=BORDER,
                        bordercolor=BG, relief="flat", arrowsize=0, width=8)

        wrap = tk.Frame(parent, bg=BG)
        wrap.pack(fill="both", expand=True)

        cv = tk.Canvas(wrap, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=cv.yview)
        cv.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        cv.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(cv, bg=BG)
        wid = cv.create_window((0, 0), window=inner, anchor="nw")

        cv.bind("<Configure>", lambda e: cv.itemconfig(wid, width=e.width))
        inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.bind_all("<MouseWheel>",
                    lambda e: cv.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        return inner

    # ── BROWSE VIEW ──────────────────────────────────────────────────────────
    def _show_browse(self):
        self._clear()
        data = load_ratings()

        # Subheader
        sh = tk.Frame(self.main, bg=BG, padx=28, pady=14)
        sh.pack(fill="x")
        tk.Label(sh, text=f"{len(KOLDSKÅL)} koldskåle", bg=BG, fg=TEXT,
                 font=self.fh2).pack(side="left")
        tk.Label(sh, text="  ·  Klik på et produkt for at se detaljer og bedømme det",
                 bg=BG, fg=TEXT_SUB, font=self.fs).pack(side="left")

        inner = self._scrollable(self.main)

        COLS = 4
        CARD_W = (self.root.winfo_screenwidth()-40)// COLS
        grid = tk.Frame(inner, bg=BG, padx=20, pady=8)
        grid.pack(fill="x")

        for i, item in enumerate(KOLDSKÅL):
            avg, cnt = get_avg(data, item["name"])
            r, c = divmod(i, COLS)
            card = self._browse_card(grid, item, avg, cnt)
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

        for c in range(COLS):
            grid.columnconfigure(c, minsize=CARD_W)

        tk.Frame(inner, bg=BG, height=24).pack()

    def _browse_card(self, parent, item, avg, cnt):
        outer = tk.Frame(parent, bg=CARD, cursor="hand2",
                         highlightbackground=BORDER, highlightthickness=1)

        # Produktbillede
        IMG_W, IMG_H = 220, 160
        photo = load_image(item["image"], IMG_W, IMG_H) or placeholder(IMG_W, IMG_H)
        img_lbl = tk.Label(outer, image=photo, bg=CARD)
        img_lbl.image = photo   # hold reference
        img_lbl.pack(fill="x")

        # Tynd separator
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x")

        body = tk.Frame(outer, bg=CARD, padx=14, pady=12)
        body.pack(fill="both", expand=True)

        COLS = 4
        CARD_W = (self.root.winfo_screenwidth()-40)// COLS

        tk.Label(body, text=item["name"], bg=CARD, fg=TEXT,
                 font=self.fn_b, wraplength=CARD_W-28, justify="left",
                 anchor="w").pack(anchor="w")
        tk.Label(body, text=item["brand"], bg=CARD, fg=TEXT_SUB,
                 font=self.fxs).pack(anchor="w", pady=(2, 8))

        if avg is not None:
            row = tk.Frame(body, bg=CARD)
            row.pack(anchor="w")
            tk.Label(row, text=f"{avg:.1f}", bg=CARD, fg=SCORE_CLR,
                     font=self.fn_b).pack(side="left")
            tk.Label(row, text=" / 10", bg=CARD, fg=TEXT_SUB,
                     font=self.fxs).pack(side="left", anchor="s", pady=1)
            # Progress bar
            bar_wrap = tk.Frame(body, bg=BAR_BG, height=10)
            bar_wrap.pack(fill="x", pady=(5, 3))
            bar_wrap.update_idletasks()
            pct = avg / 10.0
            tk.Frame(bar_wrap, bg=BAR_FG, height=10,
                     width=int(((self.root.winfo_screenwidth()-120)// COLS-28) * pct)).place(x=0, y=0)
            tk.Label(body, text=f"{cnt} {'stemme' if cnt == 1 else 'stemmer'}",
                     bg=CARD, fg=TEXT_SUB, font=self.fxs).pack(anchor="w")
        else:
            tk.Label(body, text="Ingen bedømmelser endnu", bg=CARD,
                     fg=TEXT_SUB, font=self.fxs).pack(anchor="w")

        def _enter(e):  outer.configure(highlightbackground=BORDER_HV)
        def _leave(e):  outer.configure(highlightbackground=BORDER)
        def _click(e):  self._show_detail(item)

        for w in self._all(outer):
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)
            w.bind("<Button-1>", _click)

        return outer

    # ── DETAIL VIEW ───────────────────────────────────────────────────────────
    def _show_detail(self, item):
        self._clear()
        data = load_ratings()
        avg, cnt = get_avg(data, item["name"])

        # Breadcrumb bar
        bc = tk.Frame(self.main, bg=CARD,
                      highlightbackground=BORDER, highlightthickness=0)
        bc.pack(fill="x")
        tk.Frame(bc, bg=BORDER, height=1).pack(fill="x", side="bottom")

        back = tk.Label(bc, text="← Alle koldskål", bg=CARD, fg=ACCENT,
                        font=self.fs, padx=24, pady=10, cursor="hand2")
        back.pack(side="left")
        back.bind("<Button-1>", lambda e: self._show_browse())
        back.bind("<Enter>", lambda e: back.configure(fg=ACCENT_H, font=self.fn_b))
        back.bind("<Leave>", lambda e: back.configure(fg=ACCENT, font=self.fs))

        tk.Label(bc, text=f"/ {item['brand']}  /  {item['name']}",
                 bg=CARD, fg=TEXT_SUB, font=self.fxs, pady=10).pack(side="left")

        inner = self._scrollable(self.main)
        ct = tk.Frame(inner, bg=BG, padx=40, pady=28)
        ct.pack(fill="both", expand=True)

        # ── Hero ──────────────────────────────────────────────────────────────
        hero = tk.Frame(ct, bg=CARD,
                        highlightbackground=BORDER, highlightthickness=1)
        hero.pack(fill="x", pady=(0, 22))
        tk.Frame(hero, bg=ACCENT, height=3).pack(fill="x")

        hi = tk.Frame(hero, bg=CARD, padx=28, pady=24)
        hi.pack(fill="x")

        # Billede (større i detalje-visning)
        DIMP = 400
        photo = load_image(item["image"], DIMP, DIMP) or placeholder(DIMP, DIMP)
        img_lbl = tk.Label(hi, image=photo, bg=CARD)
        img_lbl.image = photo
        img_lbl.pack(side="left", padx=(0, 28))

        meta = tk.Frame(hi, bg=CARD)
        meta.pack(side="left", fill="both", expand=True, anchor="n")
        tk.Label(meta, text=item["name"], bg=CARD, fg=TEXT,
                 font=self.fh1, wraplength=self.root.winfo_screenwidth()-456, justify="left").pack(anchor="w")
        tk.Label(meta, text=item["brand"], bg=CARD, fg=TEXT_SUB,
                 font=self.fn).pack(anchor="w", pady=(4, 0))

        # ── To kolonner ───────────────────────────────────────────────────────
        cols = tk.Frame(ct, bg=BG)
        cols.pack(fill="both", expand=True)
        cols.columnconfigure(0, minsize=(self.root.winfo_screenwidth()-120-16)//2)
        cols.columnconfigure(1, minsize=(self.root.winfo_screenwidth()-120-16)//2)

        left = tk.Frame(cols, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        # Beskrivelseskort
        self._card_block(left, "Om koldskålen",
                         item["description"], wraplength=(self.root.winfo_screenwidth()-120-16-56)//2)

        right = tk.Frame(cols, bg=BG)
        right.grid(row=0, column=1, sticky="nsew")

        # Score-kort
        sc = self._panel(right, pady=(0, 14))
        tk.Label(sc, text="Gennemsnitlig bedømmelse",
                 bg=CARD, fg=TEXT, font=self.fh3).pack(anchor="w")
        tk.Frame(sc, bg=BORDER, height=1).pack(fill="x", pady=8)

        if avg is not None:
            row = tk.Frame(sc, bg=CARD)
            row.pack(anchor="w", pady=(4, 0))
            tk.Label(row, text=f"{avg:.1f}", bg=CARD, fg=SCORE_CLR,
                     font=self.fnum).pack(side="left")
            tk.Label(row, text=" /10", bg=CARD, fg=TEXT_SUB,
                     font=self.fh2).pack(side="left", anchor="s", pady=10)

            bar_bg = tk.Frame(sc, bg=BAR_BG, height=10)
            bar_bg.pack(fill="x", pady=(10, 4))
            bar_bg.update_idletasks()
            w_px = max(bar_bg.winfo_width(), 200)
            tk.Frame(bar_bg, bg=BAR_FG, height=10,
                     width=int(w_px * avg / 10)).place(x=0, y=0)

            tk.Label(sc, text=f"Baseret på {cnt} {'stemme' if cnt == 1 else 'stemmer'}",
                     bg=CARD, fg=TEXT_SUB, font=self.fxs).pack(anchor="w", pady=(4, 0))
        else:
            tk.Label(sc, text="Ingen bedømmelser endnu",
                     bg=CARD, fg=TEXT_SUB, font=self.fn).pack(anchor="w", pady=8)

        # Rate-kort
        rc = self._panel(right)
        tk.Label(rc, text="Giv din bedømmelse",
                 bg=CARD, fg=TEXT, font=self.fh3).pack(anchor="w")
        tk.Frame(rc, bg=BORDER, height=1).pack(fill="x", pady=8)
        tk.Label(rc, text="Vælg et tal fra 0 til 10",
                 bg=CARD, fg=TEXT_SUB, font=self.fs).pack(anchor="w", pady=(2, 12))

        self.selected_rating = tk.IntVar(value=-1)
        self.rating_buttons  = []

        for row_vals in (range(0, 11),):
            rf = tk.Frame(rc, bg=CARD)
            rf.pack(anchor="w", pady=3)
            for v in row_vals:
                btn = tk.Button(
                    rf, text=str(v),
                    padx=20,
                    bg=BG, fg=TEXT, font=self.fh3,
                    relief="flat", bd=0,
                    highlightbackground=BORDER,
                    highlightthickness=1,
                    activebackground=ACCENT,
                    activeforeground="white",
                    cursor="hand2",
                    command=lambda val=v: self._pick(val, item)
                )
                btn.pack(side="left", padx=5, ipady=10)
                self.rating_buttons.append(btn)

        lrow = tk.Frame(rc, bg=CARD)
        lrow.pack(fill="x", pady=(2, 10))
        tk.Label(lrow, text="Ringe", bg=CARD, fg=TEXT_SUB, font=self.fxs).pack(side="left")
        tk.Label(lrow, text="Fremragende", bg=CARD, fg=TEXT_SUB, font=self.fxs).pack(side="right")

        self.preview_lbl = tk.Label(rc, text="", bg=CARD, fg=SCORE_CLR, font=self.fn_b)
        self.preview_lbl.pack(anchor="w")

        self.submit_btn = tk.Button(
            rc, text="Gem bedømmelse",
            state="disabled",
            bg=ACCENT, fg="white",
            font=self.fn_b,
            relief="flat", padx=18, pady=9,
            cursor="hand2",
            activebackground=ACCENT_H,
            activeforeground="white",
            command=lambda: self._submit(item)
        )
        self.submit_btn.pack(anchor="w", pady=(10, 0))

        tk.Frame(inner, bg=BG, height=32).pack()

    # ── Hjælpe-widgets ────────────────────────────────────────────────────────
    def _panel(self, parent, pady=(0, 14)) -> tk.Frame:
        """Hvidt kort med kant og padding."""
        frame = tk.Frame(parent, bg=CARD,
                         highlightbackground=BORDER, highlightthickness=1)
        frame.pack(fill="x", pady=pady)
        inner = tk.Frame(frame, bg=CARD, padx=18, pady=16)
        inner.pack(fill="x")
        return inner

    def _card_block(self, parent, title, body_text, wraplength=(1920-120-16-56)//2):
        f = self._panel(parent, pady=(0, 14))
        tk.Label(f, text=title, bg=CARD, fg=TEXT, font=self.fh3).pack(anchor="w")
        tk.Frame(f, bg=BORDER, height=1).pack(fill="x", pady=8)
        tk.Label(f, text=body_text, bg=CARD, fg=TEXT,
                 font=self.fn, wraplength=wraplength,
                 justify="left").pack(anchor="w")

    def _all(self, widget):
        res = [widget]
        for c in widget.winfo_children():
            res.extend(self._all(c))
        return res

    # ── Rating-logik ──────────────────────────────────────────────────────────
    def _pick(self, value, item):
        self.selected_rating.set(value)
        for i, btn in enumerate(self.rating_buttons):
            if i <= value:
                btn.configure(bg=ACCENT, fg="white",
                               highlightbackground=ACCENT)
            else:
                btn.configure(bg=BG, fg=TEXT,
                               highlightbackground=BORDER)
        self.preview_lbl.configure(text=f"Valgt: {value} / 10")
        self.submit_btn.configure(state="normal")

    def _submit(self, item):
        value = self.selected_rating.get()
        if value < 0:
            return
        save_rating(item["name"], value)
        messagebox.showinfo(
            "Gemt!",
            f"Du gav »{item['name']}« {value} ud af 10.\nTak for din stemme!"
        )
        self._show_detail(item)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Tjek at Pillow er installeret
    try:
        from PIL import Image  # noqa
    except ImportError:
        import tkinter.messagebox as mb
        root_tmp = tk.Tk(); root_tmp.withdraw()
        mb.showerror(
            "Manglende pakke",
            "Pillow er ikke installeret.\n\n"
            "Åbn en terminal og kør:\n    pip install pillow\n\nDerefter genstart appen."
        )
        sys.exit(1)

    root = tk.Tk()
    app = KoldskålApp(root)
    root.mainloop()