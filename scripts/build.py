#!/usr/bin/env python3
"""Compila la documentación legal Markdown a páginas estáticas para GitHub Pages."""
from __future__ import annotations
import argparse
import html
import json
import re
import unicodedata
from pathlib import Path
import mistune

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site'
CONFIG = json.loads((ROOT / 'legal-config.json').read_text(encoding='utf-8'))
DOCUMENTS = [
    ('privacy-policy', 'Política de Privacidad', 'privacy-policy.md', 'Tratamiento de datos, IA e integraciones empresariales.'),
    ('terms-of-service', 'Términos del Servicio', 'terms-of-service.md', 'Condiciones para empresas, usuarios y agentes de IA.'),
    ('data-deletion', 'Eliminación de datos', 'data-deletion.md', 'Cómo solicitar la supresión de información personal.'),
]


def incomplete_fields():
    fields = [key for key, value in CONFIG.items() if isinstance(value, str) and (not value.strip() or '[COMPLETAR' in value or '[DEFINIR' in value)]
    for key in ('privacy_email', 'support_email'):
        if key not in fields and ('@' not in CONFIG.get(key, '') or '[' in CONFIG[key]):
            fields.append(key)
    if CONFIG.get('legal_review_confirmed') is not True:
        fields.append('legal_review_confirmed (tras revisión jurídica)')
    return fields


def replace_fields(source):
    for key, value in CONFIG.items():
        if key != 'legal_review_confirmed':
            source = source.replace('{{' + key + '}}', html.escape(str(value)))
    remaining = re.findall(r'\{\{\w+\}\}', source)
    if remaining:
        raise ValueError('Claves sin definición: ' + ', '.join(set(remaining)))
    return source


def slug(text):
    text = re.sub('<[^>]+>', '', text)
    normalized = unicodedata.normalize('NFKD', html.unescape(text))
    ascii_only = ''.join(c for c in normalized if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', ascii_only.lower()).strip('-')


def build_page(slug_path, title, markdown_file, description, markdown_renderer, unfinished):
    original = (ROOT / 'content' / markdown_file).read_text(encoding='utf-8')
    body = markdown_renderer(replace_fields(original))
    anchors = []
    def replace_h2(match):
        title_inner = match.group(1)
        section_id = slug(title_inner)
        anchors.append((section_id, re.sub(r'<[^>]+>', '', title_inner)))
        return f'<h2 id="{section_id}">{title_inner}</h2>'
    body = re.sub(r'<h2>(.*?)</h2>', replace_h2, body)
    toc = '\n'.join(f'<a href="#{item_id}">{html.escape(item_title)}</a>' for item_id, item_title in anchors)
    warning = '<div class="draft" role="status"><strong>Borrador no publicable.</strong> Faltan datos reales y revisión jurídica. Completa <code>legal-config.json</code> antes de usar estas URLs en Meta.</div>' if unfinished else ''
    page = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{html.escape(description, quote=True)}"><meta name="robots" content="index,follow">
<title>{html.escape(title)} · {html.escape(CONFIG['brand'])}</title>
<link rel="stylesheet" href="../assets/styles.css"><link rel="canonical" href="" />
</head><body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="topbar"><div class="top-inner"><a class="brand" href="../" aria-label="Ir al inicio de los documentos legales"><span class="brand-mark">L</span><span>{html.escape(CONFIG['brand'])}<span class="brand-tag"> / Legal</span></span></a><nav aria-label="Documentos legales"><a href="../privacy-policy/" {'aria-current="page"' if slug_path == 'privacy-policy' else ''}>Privacidad</a><a href="../terms-of-service/" {'aria-current="page"' if slug_path == 'terms-of-service' else ''}>Términos</a><a href="../data-deletion/" {'aria-current="page"' if slug_path == 'data-deletion' else ''}>Datos</a></nav></div></header>
<div class="hero document-hero"><div class="container"><div class="eyebrow">DOCUMENTACIÓN LEGAL</div><h1>{html.escape(title)}</h1><p>{html.escape(description)}</p></div></div>
{warning}
<div class="container document-layout"><main id="main" class="legal-content" aria-label="{html.escape(title, quote=True)}">{body}</main><aside class="toc" aria-label="Índice de secciones"><div class="toc-sticky"><h3>En esta página</h3>{toc}<a class="back-top" href="#main">↑ Volver arriba</a></div></aside></div>
<footer><div class="container footer-inner"><span>© {html.escape(CONFIG['brand'])} · Información legal</span><div><a href="../privacy-policy/">Privacidad</a><a href="../terms-of-service/">Términos</a><a href="../data-deletion/">Eliminar datos</a></div></div></footer>
</body></html>'''
    destination = OUT / slug_path / 'index.html'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strict', action='store_true', help='Falla si hay datos pendientes o no hay revisión legal')
    args = parser.parse_args()
    incomplete = incomplete_fields()
    if args.strict and incomplete:
        raise SystemExit('No se puede publicar. Pendientes: ' + ', '.join(incomplete))
    renderer = mistune.create_markdown(plugins=['table'])
    for item in DOCUMENTS:
        build_page(*item, renderer, bool(incomplete))
    description = 'Textos legales y procedimientos de privacidad de una plataforma empresarial de agentes de inteligencia artificial.'
    cards = '\n'.join(
        f'<a class="doc-card" href="{url}/"><div class="doc-icon">{icon}</div><h2>{html.escape(title)}</h2><p>{html.escape(desc)}</p><span class="card-link">Leer documento <span aria-hidden="true">→</span></span></a>'
        for (url, title, _, desc), icon in zip(DOCUMENTS, ['01', '02', '03'])
    )
    warning = '<div class="draft" role="status"><strong>Borrador no publicable.</strong> Completa el fichero <code>legal-config.json</code> y valida los textos jurídicamente antes de publicarlos.</div>' if incomplete else ''
    homepage = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{html.escape(description, quote=True)}"><title>Centro legal · {html.escape(CONFIG['brand'])}</title><link rel="stylesheet" href="assets/styles.css"></head><body>
<a class="skip" href="#main">Saltar al contenido</a><header class="topbar"><div class="top-inner"><a href="./" class="brand"><span class="brand-mark">L</span><span>{html.escape(CONFIG['brand'])}<span class="brand-tag"> / Legal</span></span></a><nav aria-label="Documentos legales"><a href="privacy-policy/">Privacidad</a><a href="terms-of-service/">Términos</a><a href="data-deletion/">Datos</a></nav></div></header>
<div class="hero home-hero"><div class="container"><div class="eyebrow">TRANSPARENCIA Y CONFIANZA</div><h1>Centro legal de {html.escape(CONFIG['brand'])}</h1><p>Consulta nuestras condiciones de servicio, el tratamiento de datos y cómo ejercer tus derechos de privacidad.</p><div class="hero-meta">Última revisión del contenido: {html.escape(CONFIG['effective_date'])}</div></div></div>
{warning}<main id="main" class="container main-home"><div class="section-intro"><h2>Documentos y procedimientos</h2><p>Información accesible para organizaciones, usuarios y contactos que interactúan con nuestros servicios.</p></div><div class="cards">{cards}</div><div class="notice"><strong>¿Tienes alguna consulta?</strong><p>Para cuestiones de privacidad o sobre cómo ejercer tus derechos, consulta el procedimiento de eliminación de datos o contacta con la entidad responsable que te haya enviado el mensaje.</p></div></main>
<footer><div class="container footer-inner"><span>© {html.escape(CONFIG['brand'])} · Información legal</span><div><a href="privacy-policy/">Privacidad</a><a href="terms-of-service/">Términos</a><a href="data-deletion/">Eliminar datos</a></div></div></footer></body></html>'''
    (OUT / 'index.html').write_text(homepage, encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    print('Sitio generado en:', OUT)
    if incomplete:
        print('Pendientes antes de publicar:', ', '.join(incomplete))


if __name__ == '__main__':
    main()
