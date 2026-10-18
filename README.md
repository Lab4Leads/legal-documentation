# Lab4Leads · Documentos legales

Repositorio preparado para alojar documentos legales de **Lab4Leads** en **GitHub Pages**.

## Documentos incluidos

- `content/privacy-policy.md` — Política de Privacidad.
- `content/terms-of-service.md` — Términos del Servicio.
- `content/data-deletion.md` — Procedimiento de solicitud de eliminación de datos (útil para las integraciones de Meta).
- `legal-config.json` — datos legales y operativos que deben revisarse.
- `scripts/build.py` — generador de HTML estático.
- `site/` — web estática ya generada para previsualización; se regenera al publicar.
- `.github/workflows/deploy.yml` — publicación automática al subir cambios a `main`.

## ⚠️ Antes de publicarlo

Los textos son **borradores legales**, no una validación de cumplimiento del RGPD o de las condiciones de Meta. Deben revisarlos la entidad titular y un profesional jurídico especializado. No asumas que un punto del texto coincide con el despliegue real si aún no se ha implementado o documentado.

1. Edita `legal-config.json` y completa los campos pendientes de identidad, NIF, domicilio y emails.
2. Define los **plazos reales** de retención (conversaciones, logs, backups y eliminación de cuentas).
3. Identifica los proveedores de infraestructura, mensajería y LLM y dónde tratan datos; documenta las transferencias internacionales que procedan.
4. Revisa que la gestión de IA, WhatsApp, DPA, consentimiento, borrados y suspensión refleje los controles implementados.
5. Cuando el abogado y el responsable de la empresa lo hayan validado, cambia `legal_review_confirmed` a `true`.

**La publicación automatizada rechaza datos pendientes o falta de revisión legal**. Así se reduce el riesgo de publicar una plantilla incompleta.

## Publicación en GitHub Pages

1. Crea un repositorio de GitHub, preferiblemente dentro de la organización de Lab4Leads, con el nombre `documentos-legales`.
2. Sube todos los archivos, incluyendo el directorio oculto `.github`, a la rama `main`.
3. En **Settings → Pages → Build and deployment → Source**, selecciona **GitHub Actions**.
4. Completa `legal-config.json` y marca la revisión jurídica como realizada.
5. Haz un `push` a `main`. El workflow compilará y desplegará los documentos automáticamente.
6. En el panel **Actions** podrás verificar el resultado. En **Settings → Pages** verás la URL definitiva.

### URLs esperadas sin dominio personalizado

- `https://TU-USUARIO.github.io/documentos-legales/`
- `https://TU-USUARIO.github.io/documentos-legales/privacy-policy/`
- `https://TU-USUARIO.github.io/documentos-legales/terms-of-service/`
- `https://TU-USUARIO.github.io/documentos-legales/data-deletion/`

Sustituye `TU-USUARIO` por el propietario real del repositorio (usuario u organización). Estas URL son **ejemplos** y no funcionarán hasta publicar.

### Dominio personalizado (opcional)

Puedes configurar `legal.TU-DOMINIO.com` desde **Settings → Pages → Custom domain** y luego añadir en tu DNS un registro CNAME que apunte a `TU-USUARIO.github.io`. Verifica la propiedad del dominio y activa HTTPS. No añadas manualmente un fichero `CNAME` si publicas mediante este workflow de Actions.

## Edición y previsualización local

Para cambiar un documento, edita su fichero Markdown en `content/`. No edites directamente los HTML generados dentro de `site/`, porque se sobrescriben durante el despliegue.

```bash
python3 -m pip install 'mistune==3.1.3'
python3 scripts/build.py
python3 -m http.server 8000 --directory site
```

Abre `http://localhost:8000/`. Si hay campos pendientes aparecerá un aviso de **borrador**.

Para verificar que la publicación está permitida:

```bash
python3 scripts/build.py --strict
```

## Configuración recomendada para Meta

En **Meta for Developers → App settings → Basic** establece:

- **Privacy Policy URL:** URL HTTPS pública de `/privacy-policy/`.
- **Terms of Service URL:** URL HTTPS pública de `/terms-of-service/`.
- **User Data Deletion:** si el flujo de tu aplicación usa instrucciones/URL de eliminación de datos, enlaza `/data-deletion/` y confirma que la vía de solicitud funciona realmente.

No introduzcas secretos, tokens, claves de Meta, información personal de clientes ni datos confidenciales en este repositorio público.

## Alcance jurídico adicional

Estos tres documentos **no sustituyen** el DPA con empresas clientes, la política de cookies específica si se usan cookies no esenciales, las instrucciones de consentimiento para mensajes comerciales, ni las cláusulas empresariales o políticas que Meta requiera para determinados flujos.
