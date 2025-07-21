
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
      <h1 class="welcome-title">{module}</h1>
    </div>"""
    return ret


HOME_BUTTON = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@900&display=swap');

div.stButton > button[kind="primary"] {
  font-family: 'Rubik', sans-serif !important;
  font-size: 20px !important;
  font-weight: 900 !important;
  height: 30px !important;
  padding: 0 40px !important;
  width: 30px !important;
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

STUDY_BUTTON = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@900&display=swap');

div.stButton > button[kind="secondary"] {
  font-family: 'Rubik', sans-serif !important;
  font-size: 20px !important;
  font-weight: 900 !important;
  height: 60px !important;
  padding: 0 40px !important;
  min-width: 300px !important;
  border-radius: 8px !important;
  background-color: #fff1e6 !important;
  color: #111 !important;
  border: 2px solid #111 !important;
  position: relative !important;
  cursor: pointer !important;
  transition: transform .2s !important;
  box-sizing: border-box !important;
  box-shadow: 8px 8px 0 #e0b8a1 !important;
  overflow: visible !important;
}

div.stButton > button[kind="secondary"]:hover {
  box-shadow: none !important;
  transform: translate(8px, 8px) !important;
}

div.stButton > button[kind="secondary"]:active {
  background-color: #ffdeda !important;
  transform: translate(4px, 4px) !important;
}

div.stButton > button[kind="secondary"]:focus {
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(207, 220, 240, 1) !important;
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

EXAM_BUTTON = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@900&display=swap');

div.stButton > button[kind="tertiary"] {
  font-family: 'Rubik', sans-serif !important;
  font-size: 20px !important;
  font-weight: 900 !important;
  height: 60px !important;
  padding: 0 40px !important;
  min-width: 300px !important;
  border-radius: 8px !important;
  background-color: #e3f0fe !important;
  color: #111 !important;
  border: 2px solid #111 !important;
  position: relative !important;
  cursor: pointer !important;
  transition: transform .2s !important;
  box-sizing: border-box !important;
  box-shadow: 8px 8px 0 #a1bce0 !important;
  overflow: visible !important;
}

div.stButton > button[kind="tertiary"]:hover {
  box-shadow: none !important;
  transform: translate(8px, 8px) !important;
}

div.stButton > button[kind="tertiary"]:active {
  background-color: #ffdeda !important;
  transform: translate(4px, 4px) !important;
}

div.stButton > button[kind="tertiary"]:focus {
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(207, 220, 240, 1) !important;
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

TEXT_NO_EXAM = """
<!-- load Poppins from Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">

<style>
  .spacer-20  { margin-top:60px !important; }

  /* our “you haven’t taken it” message */
  .exam-prompt {
    font-family: 'Poppins', sans-serif !important;
    /* scale between 1.2rem–2rem depending on viewport */
    font-size: clamp(0.9rem, 1.5vw, 1.1rem) !important;
    font-weight: 600 !important;
    color: #f0f0f0 !important;        /* light grey on dark bg */
    text-align: center !important;
    margin: 1rem auto 1.5rem auto !important; /* some breathing room */
    max-width: 80%;                   /* don’t let it run full width */
  }
</style>

<div class="spacer-20"></div>
<div class="exam-prompt">
  You haven’t done your mock exam
</div>
"""

METRIC_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">

<style>
.custom-metric-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
}

.custom-metric-wrapper .metric-container {
  background-color: #E6E6FA;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  /* you wanted “span width” instead of height: */
  width: 100%;
  max-width: 240px;
  /* top-margin was your spacer; bottom-margin gives gap to GIF */
  margin: 60px 0 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Poppins', sans-serif;
}

.metric-label  { font-size: 0.9rem; color: #555; margin-bottom: 0.25rem; }
.metric-value  { font-size: 2.5rem; font-weight: 600; color: #333; margin-bottom: 0.25rem; }
.metric-delta  { font-size: 1rem; color: #9370DB; }
</style>
"""