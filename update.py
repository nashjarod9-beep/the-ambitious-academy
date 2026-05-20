import os
import re

def update_guarantee(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_guarantee = r'"Si après avoir suivi avec sérieux la formation tu n\'es pas pleinement satisfait de la méthode, contacte-nous dans les 30 jours suivant ton achat et nous te remboursons intégralement chaque centime versé. Sans question. Sans condition."'
    new_guarantee = '"Si après avoir suivi et mis en pratique, tu n\'as pas de résultat, écris-moi avec les preuves de ta mise en pratique et je t\'offre une autre formation ou je te rends ton argent."'
    
    content = re.sub(old_guarantee, new_guarantee, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update guarantee in all HTML files
for file in os.listdir('.'):
    if file.endswith('.html'):
        update_guarantee(file)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add "Formation + un accompagnement personnel premium" in Hero
hero_promo = r'(<div class="badge-promo" id="hero-promo-badge">\s*<span></span>)🔥 Nouvelle Promotion — 48h Seulement(\s*</div>)'
new_hero_promo = r'\1🔥 Formation + un accompagnement personnel premium\2'
html = re.sub(hero_promo, new_hero_promo, html)

# 2. Change Hero button text
old_btn = r'🚀 JE VEUX VENDRE MAINTENANT — 8\.500 FCFA'
new_btn = r'🚀 Je veux ce programme complet S.A.C.C.'
html = re.sub(old_btn, new_btn, html)

# 3. Extract sections
# Let's use regex to extract sections.
# Format: <!-- NAME -->\s*<section ...>...</section>
def extract_section(html, section_id):
    pattern = re.compile(r'(<!-- .*? -->\s*<section .*?id="' + section_id + r'".*?</section>)', re.DOTALL)
    match = pattern.search(html)
    if match:
        return match.group(1), pattern
    return None, None

hero_html, hero_pat = extract_section(html, 'home')
problemes_html, problemes_pat = extract_section(html, 'problemes')
temoignages_html, temoignages_pat = extract_section(html, 'temoignages')
agitation_html, agitation_pat = extract_section(html, 'agitation')

# Remove these sections from the original html temporarily to re-insert them in order
if problemes_pat: html = problemes_pat.sub('<!-- PLACEHOLDER_PROBLEMES -->', html)
if temoignages_pat: html = temoignages_pat.sub('<!-- PLACEHOLDER_TEMOIGNAGES -->', html)
if agitation_pat: html = agitation_pat.sub('<!-- PLACEHOLDER_AGITATION -->', html)

# Split temoignages into images only and then text only
# We will create a new HTML for temoignages
new_temoignages_html = """
  <!-- SOCIAL PROOF SECTION (Section 3) -->
  <section class="section section-dark-secondary bg-grain" id="temoignages">
    <div class="container">
      <div class="section-header scroll-reveal">
        <span class="label-text">Ce que disent nos étudiants</span>
        <h2 class="section-title">Ils ont fait le premier pas. Voici leur retour.</h2>
      </div>
      
      <!-- DESKTOP GRID - IMAGES ONLY -->
      <div class="testimonials-grid scroll-reveal stagger-1" style="margin-bottom: 50px;">
        <div class="testimonial-card"><img src="./témoignages/IMG_0039.jpg" style="width:100%; border-radius: 12px;"></div>
        <div class="testimonial-card"><img src="./témoignages/IMG_0062.jpg" style="width:100%; border-radius: 12px;"></div>
        <div class="testimonial-card"><img src="./témoignages/IMG_1902.jpg" style="width:100%; border-radius: 12px;"></div>
        <div class="testimonial-card"><img src="./témoignages/IMG_1989.jpg" style="width:100%; border-radius: 12px;"></div>
        <div class="testimonial-card"><img src="./témoignages/IMG_2828.jpg" style="width:100%; border-radius: 12px;"></div>
        <div class="testimonial-card"><img src="./témoignages/IMG_2829.jpg" style="width:100%; border-radius: 12px;"></div>
      </div>
      
      <div class="section-header scroll-reveal" style="margin-top: 60px;">
        <span class="label-text" style="color: var(--gold-accent); font-weight: bold;">+900 personnes formés</span>
        <h2 class="section-title">85 % d'avis positifs certifiés</h2>
      </div>

      <!-- TEXT REVIEWS -->
      <div class="grid grid-3 scroll-reveal stagger-1">
        <div class="testimonial-card" style="padding: 20px;">
            <div class="testimonial-rating">★★★★★</div>
            <p class="testimonial-quote">"Impécable 👍🏽. Contenu très clair et direct au but."</p>
            <h4 class="testimonial-author">Julienne L.</h4>
        </div>
        <div class="testimonial-card" style="padding: 20px;">
            <div class="testimonial-rating">★★★★★</div>
            <p class="testimonial-quote">"Contenu du cours bien détaillé pour faciliter la compréhension et le lancement rapide."</p>
            <h4 class="testimonial-author">Binetou G.</h4>
        </div>
        <div class="testimonial-card" style="padding: 20px;">
            <div class="testimonial-rating">★★★★★</div>
            <p class="testimonial-quote">"Je n'y croyais pas mais la méthode d'acquisition WhatsApp est redoutable !"</p>
            <h4 class="testimonial-author">Étudiant Vérifié</h4>
        </div>
      </div>

    </div>
  </section>
"""

new_vs_section = """
  <!-- VS SECTION -->
  <section class="section section-dark bg-grain" id="comparatif">
    <div class="container">
      <div class="section-header scroll-reveal">
        <span class="label-text">La Réalité du Marché</span>
        <h2 class="section-title">Ce que les gens t'ont fait croire <span class="text-red">VS</span> Ce qu'il en est réellement</h2>
      </div>

      <div class="grid grid-2 scroll-reveal stagger-1">
        <div class="pain-card" style="border: 1px solid #444;">
          <div class="pain-icon-wrapper"><span class="pain-icon">❌</span></div>
          <div class="pain-content">
            <h4 class="pain-title">Ce qu'on t'a fait croire</h4>
            <p class="pain-text">"Il te suffit d'avoir une jolie boutique avec quelques produits pour que les clients achètent tout seuls."</p>
          </div>
        </div>
        <div class="pain-card" style="border: 1px solid var(--primary-red);">
          <div class="pain-icon-wrapper" style="background: rgba(229, 9, 20, 0.1);"><span class="pain-icon">✅</span></div>
          <div class="pain-content">
            <h4 class="pain-title">Ce qu'il en est réellement</h4>
            <p class="pain-text">Une boutique sans trafic qualifié et sans système d'acquisition (S.A.C) est une boutique morte. Il faut un tunnel de vente clair, des offres irrésistibles et des relances automatisées.</p>
          </div>
        </div>
        
        <div class="pain-card" style="border: 1px solid #444;">
          <div class="pain-icon-wrapper"><span class="pain-icon">❌</span></div>
          <div class="pain-content">
            <h4 class="pain-title">Ce qu'on t'a fait croire</h4>
            <p class="pain-text">"Poste tous les jours sur TikTok ou Instagram et tu deviendras riche en un mois."</p>
          </div>
        </div>
        <div class="pain-card" style="border: 1px solid var(--primary-red);">
          <div class="pain-icon-wrapper" style="background: rgba(229, 9, 20, 0.1);"><span class="pain-icon">✅</span></div>
          <div class="pain-content">
            <h4 class="pain-title">Ce qu'il en est réellement</h4>
            <p class="pain-text">Poster sans stratégie d'acquisition ne rapporte que des vues, pas de l'argent. Il te faut convertir ces vues en prospects puis en clients via WhatsApp ou l'Emailing.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

# Re-insert sections in the correct order:
# The original order after HERO was: TEMOIGNAGES -> PROBLEMES -> AGITATION
# New order: HERO -> PROBLEMES -> TEMOIGNAGES -> AGITATION -> VS SECTION

# Let's rebuild the sequence after HERO
insertion_marker = '<!-- PLACEHOLDER_TEMOIGNAGES -->' # the first one after hero originally

# We remove the placeholders
html = html.replace('<!-- PLACEHOLDER_PROBLEMES -->', '')
html = html.replace('<!-- PLACEHOLDER_AGITATION -->', '')

# Insert the sequence at the first placeholder
sequence = problemes_html + '\n' + new_temoignages_html + '\n' + agitation_html + '\n' + new_vs_section
html = html.replace('<!-- PLACEHOLDER_TEMOIGNAGES -->', sequence)


# 7. Update Bonuses in Bonus Section
# Bonus 1
html = re.sub(r'Liste des 50 idées de produits digitaux rentables', 'Liste de 100 idées de produits digitaux', html)
html = re.sub(r'Liste des 50 idées de produits digitaux \(Val. 5.000 FCFA\)', 'Liste de 100 idées de produits digitaux (Val. 5.000 FCFA)', html)
html = re.sub(r'Reçois 50 idées validées', 'Reçois 100 idées validées', html)

# Bonus 2
html = re.sub(r'<h3 class="bonus-title">Ebooks Marketing Premium</h3>', '<h3 class="bonus-title">La masterclass Chariow Ultra complète</h3>', html)
html = re.sub(r'Bonus 2 : Ebooks Marketing Premium \(Val. 7.500 FCFA\)', 'Bonus 2 : La masterclass Chariow Ultra complète (Val. 7.500 FCFA)', html)
html = re.sub(r'Les meilleures stratégies de vente directe et de copywriting distillées dans des guides d\'action clairs, immédiatement applicables pour booster ton business.', 'Une masterclass exclusive et intensive pour maîtriser de A à Z les stratégies avancées du système Chariow.', html)

# Bonus 3
html = re.sub(r'<h3 class="bonus-title">Chatbot WhatsApp pré-configuré</h3>', '<h3 class="bonus-title">Formation Comment créer un agent IA WhatsApp</h3>', html)
html = re.sub(r'Bonus 3 : Chatbot WhatsApp pré-configuré \(Val. 15.000 FCFA\)', 'Bonus 3 : Formation Comment créer un agent IA WhatsApp (Val. 15.000 FCFA)', html)

# Bonus 4
html = re.sub(r'<h3 class="bonus-title">Stratégies de Vente Rapide</h3>', '<h3 class="bonus-title">Ebook mes 10 conseils stratégiques de vente de produits digitaux</h3>', html)
html = re.sub(r'Bonus 4 : Stratégies de Vente Rapide \(Val. 10.000 FCFA\)', 'Bonus 4 : Ebook mes 10 conseils stratégiques de vente de produits digitaux (Val. 10.000 FCFA)', html)
html = re.sub(r'Les tactiques éprouvées en coulisses pour générer tes toutes premières ventes de produits digitaux dans les 7 premiers jours suivant le lancement.', 'Mes 10 conseils en or, tirés de l\'expérience du terrain, pour maximiser tes ventes.', html)

# Remove "Accès à vie illimité aux futures mises à jour"
html = re.sub(r'<li class="offer-check-item">\s*<span class="offer-check-icon">✅</span>\s*<span>Accès à vie illimité aux futures mises à jour du programme</span>\s*</li>', '', html)
html = re.sub(r'<li class="offer-check-item">\s*<span class="offer-check-icon">✅</span>\s*<span>Accès à vie illimité aux futures mises à jour</span>\s*</li>', '', html)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Modification complete!")
