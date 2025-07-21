def make_main_title(module):
    ret = f"""<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
    .welcome-container {{
      position: relative !important;
      width: 100vw !important;
      margin-left: calc(50% - 50vw) !important;
      display: flex !important;
      justify-content: center !important;
      padding: 2rem 0 !important;
    }}
    .welcome-title {{
      position: relative;
      font-family: 'Playfair Display', serif !important;
      font-size: clamp(1.5rem, 4vw, 3rem) !important;
      white-space: nowrap !important;
      line-height: 1 !important;
      background: linear-gradient(45deg, #ff6ec4, #7873f5, #2b86c5) !important;
      background-size: 300% 300% !important;
      -webkit-background-clip: text !important;
      -webkit-text-fill-color: transparent !important;
      text-shadow: 3px 3px 12px rgba(0,0,0,0.3) !important;
      animation: gradientShift 6s ease infinite !important;
    }}
    @keyframes gradientShift {{
      0%   {{ background-position: 0% 50%; }}
      50%  {{ background-position: 100% 50%; }}
      100% {{ background-position: 0% 50%; }}
    }}
    .welcome-title::after {{
      content: '';
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      pointer-events: none;
      background:
        radial-gradient(circle at 10% 20%, #fff 2px, transparent 0),
        radial-gradient(circle at 20% 60%, #fff 2px, transparent 0),
        radial-gradient(circle at 30% 30%, #fff 2px, transparent 0),
        radial-gradient(circle at 40% 75%, #fff 2px, transparent 0),
        radial-gradient(circle at 50% 10%, #fff 2px, transparent 0),
        radial-gradient(circle at 60% 50%, #fff 2px, transparent 0),
        radial-gradient(circle at 70% 25%, #fff 2px, transparent 0),
        radial-gradient(circle at 80% 65%, #fff 2px, transparent 0),
        radial-gradient(circle at 90% 40%, #fff 2px, transparent 0),
        radial-gradient(circle at 25% 40%, #fff 2px, transparent 0);
      background-repeat: no-repeat;
      mix-blend-mode: screen;
      opacity: 0;
      animation: sparkle 1.5s linear infinite;
    }}
    @keyframes sparkle {{
      0%,20%,100%   {{ opacity: 0; }}
      5%,15%        {{ opacity: 1; }}
      30%,40%       {{ opacity: 0; }}
      45%,55%       {{ opacity: 1; }}
      60%,80%       {{ opacity: 0; }}
      85%,95%       {{ opacity: 1; }}
    }}
    </style>
    <div class="welcome-container">
      <h1 class="welcome-title">Currently studying: {module}</h1>
    </div>"""
    return ret


BACK_BUTTON = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@900&display=swap');

div.stButton > button[kind="primary"] {
  font-family: 'Rubik', sans-serif !important;
  font-size: 20px !important;
  font-weight: 900 !important;
  height: 30px !important;
  padding: 0 40px !important;
  min-width: 40px !important;
  border-radius: 8px !important;
  background-color: #ffe2f0 !important;
  color: #111 !important;
  border: 2px solid #111 !important;
  position: relative !important;
  cursor: pointer !important;
  transition: transform .2s !important;
  box-sizing: border-box !important;
  box-shadow: 8px 8px 0 #d6a6ba !important;
  overflow: visible !important;
}

div.stButton > button[kind="primary"]:hover {
  box-shadow: none !important;
  transform: translate(8px, 8px) !important;
}

div.stButton > button[kind="primary"]:active {
  background-color: #ffdeda !important;
  transform: translate(4px, 4px) !important;
}

div.stButton > button[kind="primary"]:focus {
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(190, 140, 160, 1) !important;
}

div.stButton button > p {
  background: none !important;
  box-shadow: none !important;
  border: none !important;
  padding: 0 !important;
  margin: 0 !important;
  transform: none !important;
}
</style>
"""

CUSTOM_TAB = """
<style>
  .stTabs [data-baseweb="tab-list"] {
    display: flex;
    gap: 2px;
    font-family: 'Roboto', sans-serif;  /* better font */
  }
  
  .stTabs [data-baseweb="tab"] {
    flex: 1;
    text-align: center;
    height: 50px;
    white-space: pre-wrap;
    background-color: #e3f0fe;
    border-radius: 4px 4px 0 0;
    padding: 10px 0;
    color: black;
    font-size: 16px;
    min-width: 0;
    border-bottom: 3px solid transparent;  /* reserve space for the highlight */
  }

  .stTabs [data-baseweb="tab"]:hover {
    background-color: #d1e5fa;
    cursor: pointer;
  }

  .stTabs [aria-selected="true"] {
    background-color: #a1bce0;               /* you can tweak this to a darker shade */
    border-bottom: 3px solid #003366;        /* dark blue “underline” */
    color: black;                            /* ensure text stays black */
  }
</style>
"""


