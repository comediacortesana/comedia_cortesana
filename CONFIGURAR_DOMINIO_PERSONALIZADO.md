# 🌐 Configurar Dominio Personalizado en GitHub Pages

## Situación Actual

**Tu dominio:** `comediacortesana.es`  
**Error actual:** "DNS check unsuccessful"  
**Causa:** Los registros DNS no están configurados correctamente

---

## ✅ Solución: Configurar DNS

### Paso 1: Identificar tu proveedor de dominio

¿Dónde compraste `comediacortesana.es`?
- GoDaddy
- Namecheap
- Google Domains
- DonDominio (España)
- Otro

---

### Paso 2: Añadir registros DNS

Necesitas acceder al panel de control de tu proveedor y añadir estos registros:

#### **Opción A: Dominio Apex (comediacortesana.es)**

Añade estos 4 registros tipo **A**:

| Tipo | Host/Name | Valor/Points to | TTL |
|------|-----------|-----------------|-----|
| A    | @         | 185.199.108.153 | 3600 |
| A    | @         | 185.199.109.153 | 3600 |
| A    | @         | 185.199.110.153 | 3600 |
| A    | @         | 185.199.111.153 | 3600 |

#### **Opción B: Con www (www.comediacortesana.es)**

Añade un registro **CNAME**:

| Tipo  | Host/Name | Valor/Points to        | TTL |
|-------|-----------|------------------------|-----|
| CNAME | www       | thygolem.github.io     | 3600 |

**Recomendación:** Usa ambas opciones para que funcione con y sin www

---

## 🔧 Instrucciones por Proveedor

### **GoDaddy**
1. Inicia sesión en GoDaddy
2. Mis productos → DNS → Administrar
3. Click "Añadir" en la sección de registros
4. Añade los registros A (arriba)
5. Guarda cambios

### **Namecheap**
1. Inicia sesión en Namecheap
2. Domain List → Manage → Advanced DNS
3. Click "Add New Record"
4. Añade los registros A
5. Save All Changes

### **Google Domains**
1. Inicia sesión en Google Domains
2. Selecciona tu dominio → DNS
3. Registros de recursos personalizados
4. Añade los registros A
5. Guardar

### **DonDominio (España)**
1. Inicia sesión en DonDominio
2. Mis dominios → Gestión DNS
3. Añadir registro
4. Añade los registros A
5. Guardar cambios

### **Cloudflare (si lo usas)**
1. Inicia sesión en Cloudflare
2. Selecciona tu dominio → DNS
3. Add record
4. Añade los registros A
5. ⚠️ IMPORTANTE: Desactiva el proxy (nube gris, no naranja) temporalmente
6. Save

---

## ⏰ Tiempo de Propagación

⚠️ **Importante:** Los cambios DNS pueden tardar:
- **Mínimo:** 1-2 horas
- **Normal:** 24 horas
- **Máximo:** 48 horas

Durante este tiempo:
- Usa la URL temporal de GitHub: `https://thygolem.github.io/comedia_cortesana/`
- No hagas cambios repetidos (puede alargar la propagación)
- Sé paciente 😊

---

## ✓ Verificar Configuración

### Método 1: Herramienta Online
Usa esta herramienta para verificar DNS:
- https://www.whatsmydns.net/
- Busca: `comediacortesana.es`
- Debe mostrar las IPs de GitHub (185.199.108-111.153)

### Método 2: Terminal (Mac/Linux)
```bash
# Verificar registros A
dig comediacortesana.es +short

# Debe mostrar:
# 185.199.108.153
# 185.199.109.153
# 185.199.110.153
# 185.199.111.153

# Verificar CNAME (si usas www)
dig www.comediacortesana.es +short
# Debe mostrar: thygolem.github.io
```

### Método 3: En GitHub
1. Vuelve a Settings → Pages
2. Click "Check again" en el error
3. Si está bien configurado, verás ✅ "DNS check successful"

---

## 🚀 Después de Configurar DNS

### En GitHub Pages:

1. **Mantén** `comediacortesana.es` en el campo Custom domain
2. Click **"Save"** (aunque siga con error inicialmente)
3. **Espera** 24 horas para propagación
4. Vuelve y click **"Check again"**
5. Cuando funcione, activa **"Enforce HTTPS"** (recomendado)

### HTTPS (Certificado SSL)
- GitHub genera un certificado SSL gratis automáticamente
- Puede tardar unas horas adicionales después del DNS
- Cuando esté listo, marca ✅ "Enforce HTTPS"

---

## 💰 Costos

| Concepto | Costo |
|----------|-------|
| **GitHub Pages** | 🆓 $0/año (Gratis) |
| **Dominio .es** | 💰 ~€8-15/año |
| **Certificado SSL** | 🆓 $0 (GitHub lo da gratis) |

**Total anual:** Solo el costo del dominio (~€10/año)

---

## 🎯 Opción Alternativa: Sin Dominio Personalizado

Si prefieres no gastar en dominio, puedes usar la URL gratuita de GitHub:

### URL Gratuita:
```
https://thygolem.github.io/comedia_cortesana/
```

**Ventajas:**
- ✅ Completamente gratis
- ✅ Funciona inmediatamente
- ✅ HTTPS incluido
- ✅ No requiere configuración DNS

**Desventajas:**
- ⚠️ URL más larga
- ⚠️ Menos "profesional"

---

## 🆘 Problemas Comunes

### Error persiste después de 48 horas

**Causas posibles:**
1. **Registros mal configurados**
   - Verifica que las IPs sean exactamente: 185.199.108-111.153
   - El Host debe ser "@" o vacío (no "comediacortesana.es")

2. **DNS caché**
   - Limpia caché DNS en tu Mac:
   ```bash
   sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
   ```

3. **Proveedor no permite Apex domain**
   - Algunos proveedores no permiten registros A en el apex
   - Solución: Usa solo www.comediacortesana.es

4. **Cloudflare activo**
   - Si usas Cloudflare, desactiva el proxy (nube gris)
   - Después de que funcione, puedes reactivarlo

### "Not served over HTTPS"
- Normal al inicio
- Espera 24h más para que GitHub genere el certificado
- Luego activa "Enforce HTTPS"

### "Repository cannot be accessed using the custom domain"
- Verifica que el repo sea público
- Verifica que GitHub Pages esté activado
- El archivo debe llamarse `index.html`

---

## 📋 Checklist Completo

- [ ] Dominio comprado y activo
- [ ] Acceso al panel DNS del proveedor
- [ ] Registros A añadidos (4 IPs de GitHub)
- [ ] (Opcional) Registro CNAME para www añadido
- [ ] Guardados los cambios en el proveedor
- [ ] Esperado al menos 2-4 horas
- [ ] Verificado DNS con whatsmydns.net o dig
- [ ] Click en "Check again" en GitHub
- [ ] DNS check successful ✅
- [ ] Esperado certificado SSL (24h más)
- [ ] Activado "Enforce HTTPS"
- [ ] Sitio funcionando en dominio personalizado 🎉

---

## 🎉 Resultado Final

Cuando todo esté configurado correctamente:

**Tus URLs funcionarán:**
- ✅ https://comediacortesana.es
- ✅ https://www.comediacortesana.es (si configuraste CNAME)
- ✅ https://thygolem.github.io/comedia_cortesana/ (sigue funcionando)

**Con:**
- 🔒 HTTPS automático
- ⚡ Carga rápida
- 🆓 Hosting gratis
- 🔄 Actualizaciones fáciles con git push

---

## 💡 Recomendación

Si no necesitas el dominio personalizado urgentemente:

1. **Por ahora:** Usa `thygolem.github.io/comedia_cortesana/`
2. **Mientras:** Configura DNS con calma
3. **Espera:** 48 horas de propagación
4. **Luego:** Cambia al dominio personalizado

El sitio funciona perfectamente con la URL de GitHub mientras tanto.

---

## 📞 Recursos Útiles

- **Documentación oficial GitHub:** https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
- **Verificar DNS:** https://www.whatsmydns.net/
- **Verificar propagación:** https://dnschecker.org/
- **Ayuda GitHub Pages:** https://pages.github.com/

---

**¿Prefieres usar la URL gratuita de GitHub?**  
Simplemente haz click en **"Remove"** junto a `comediacortesana.es` y usa:  
`https://thygolem.github.io/comedia_cortesana/` ✅

