# مبدأ تحقق الإيراد – Revenue Recognition Principle (20 ثانية، 9:16)

Episode 2 of the series «المحاسبة في 15 ثانية». It keeps the same visual identity as episode 1 (`../accrual-basis-video`): the same palette, fonts, office setting, light-streak transitions, calendar, film grain and score.

| Output | Spec |
| --- | --- |
| `out/revenue-recognition-4k.mp4` | 2160×3840, 30 fps, exactly 20.0 s, H.264 High, AAC 256k, −14 LUFS / −1 dBTP |
| `out/revenue-recognition-1080p.mp4` | 1080×1920 upload copy |
| `out/cover.jpg` | Title card (3.0 s) |

## Storyboard (as built)

| Time | Scene | On-screen text | Voice-over |
| --- | --- | --- | --- |
| 0–4 s | Night office; slow push-in over a service contract and an invoice (10,000 دينار) on the desk; monitor out of focus behind | «متى نعترف بالإيراد محاسبيًا؟» + series badge «المحاسبة في 15 ثانية · الحلقة 2» | متى نعترف بالإيراد؟ |
| 4–10 s | Camera dives into the contract → service card (10,000 دينار, performance obligation: deliver the service in full) → progress bar fills to 100% → green badge «تم الوفاء بالتزام الأداء» → date 20 أكتوبر 2026 | «تم تقديم الخدمة في 20 أكتوبر» | عندما نفي بالتزامنا تجاه العميل، ونقدم له السلعة أو الخدمة. |
| 10–16 s | Calendar: 20 Oct gets a green check; the page flips to November; 18 Nov gets a cash marker. A timeline links the two dates (29 days apart) | «تحقق الإيراد: 10,000 دينار» · «استلام النقدية: 10,000 دينار» · «المعيار: الوفاء بالتزام الأداء — لا تاريخ الفاتورة ولا تاريخ التحصيل» | مش شرط عند إصدار الفاتورة، أو استلام المقابل المالي. |
| 16–20 s | October income statement with «إيرادات الخدمات 10,000 دينار» highlighted, plus a light sweep | «الإيراد يُعترف به عند الوفاء بالتزام الأداء» then «افهم المحاسبة.. لا تكتفِ بتسجيل الأرقام» | المهم: متى تحقق الإيراد محاسبيًا. |

## Accounting checks (IFRS 15)

- One amount everywhere: **10,000 دينار** on the invoice, the service card, both timeline labels and the income statement.
- Revenue is recognised on **20 October**, when the performance obligation is satisfied in full (a service satisfied at a point in time, as the brief assumes). The October income statement carries the revenue.
- Cash is received on **18 November**. It is labelled only as cash receipt, not as revenue.
- No invoice date is shown, so invoicing isn't confused with recognition. The scene 3 caption states the rule: neither the invoice date nor the collection date decides recognition.
- No journal entries are shown.
- The calendars are real 2026 dates with a Saturday week start (1 Oct = Thursday, 1 Nov = Sunday).

## Voice-over

- The narration uses your script exactly as written, including «مش شرط», at a natural pace with no time-stretching. It runs about 16.4 s of speech inside the 20 s.
- The voice is offline piper TTS (`ar_JO-kareem-medium`, Arabic male).
- To use your own recorded voice, replace `.work/voice.wav` (20 s, 48 kHz) and re-run step 3 of `build.sh`.

## Rebuild

```bash
VOICE_MODEL=/path/to/ar_JO-kareem-medium.onnx ./build.sh [workdir]
```

Preview any moment with `scene.html?t=12.8`.

## Suggested post caption

> متى نعترف بالإيراد؟ عندما نفي بالتزامنا تجاه العميل ونقدم له السلعة أو الخدمة — مش شرط عند إصدار الفاتورة أو استلام المقابل المالي.
> المثال: خدمة بقيمة 10,000 دينار قُدّمت في 20 أكتوبر وحُصّلت في 18 نوفمبر ← الإيراد يُسجَّل في أكتوبر.
>
> #المحاسبة_في_15_ثانية #تحقق_الإيراد #IFRS15 #محاسبة #RevenueRecognition #Accounting
