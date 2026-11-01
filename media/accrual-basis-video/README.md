# مبدأ الاستحقاق — فيديو تعليمي 15 ثانية (9:16)

Vertical educational reel on the **Accrual Basis of Accounting** for LinkedIn / Facebook / Instagram.

| Output | Spec |
| --- | --- |
| `out/accrual-basis-4k.mp4` | 2160×3840 (4K UHD vertical), 30 fps, H.264 High, AAC 256k, −14 LUFS / −1 dBTP |
| `out/accrual-basis-1080p.mp4` | 1080×1920 upload-optimised copy (Instagram Reels re-encodes to 1080p anyway) |
| `out/cover.jpg` | Thumbnail frame (title card at 3.2 s) |

## Storyboard (as built)

| Time | Scene | On-screen text | Voice-over |
| --- | --- | --- | --- |
| 0–4 s | Over-the-shoulder shot of an accountant in a night office; slow dolly push-in to a monitor showing an October report with invoice 1024 (10,000) highlighted | «هل تعرف متى يُعترف بالإيراد محاسبيًا؟» | هل تعلم أن الإيراد لا يُسجَّل بالضرورة عند استلام النقود؟ |
| 4–9.4 s | Camera dives into the screen → service card (October) → invoice 10,000 دينار counts up → stamp «لم تُحصَّل بعد» → «استلام المبلغ مؤجَّل إلى نوفمبر» | «مبدأ الاستحقاق يعني تسجيل الإيراد عند تحققه، وليس عند استلام النقدية» | مبدأ الاستحقاق: الإيراد يُسجَّل عند تحققه، والمصروف عند نشوئه، |
| 9.4–13 s | Calendar: 20 October highlighted (revenue recognised) → page flips to November, 18 November highlighted (cash collected). Timeline: October = revenue recorded; November = cash collection, settles receivable, **no new revenue** | «العبرة بتاريخ تحقق الإيراد أو نشوء المصروف، وليس بتاريخ الدفع أو القبض» | بغضّ النظر عن موعد القبض أو الدفع. |
| 13–15 s | Three financial statements (income statement, financial position, cash flows) fan in with a gold light sweep | «مبدأ الاستحقاق... أساس القوائم المالية الدقيقة» | ببساطة: نسجّل النشاط وقت حدوثه. |

### Accounting accuracy

- No journal entries are shown on screen. The only treatment stated is the correct one: revenue recognised in October when the service is delivered (against a receivable); November collection settles the receivable and **does not create revenue**.
- The invoice date (20 Oct), the highlighted calendar day, and the collection month (November) all agree.
- Calendar grids are real 2026 dates with a Saturday week start (1 Oct 2026 = Thursday, 1 Nov 2026 = Sunday).

### Voice-over script

The proposed script is about 20 s at a natural pace. It was tightened to fit 15 s without changing its meaning. The full script is still used for the video's caption (below).

## Design

- Palette: dark navy `#071327 / #0b1f3f / #12305e`, white, gold `#d4af5a / #e9cf8a`.
- Type: **Tajawal** ExtraBold (headlines), **Cairo** (UI). Both are SIL OFL fonts, bundled in `fonts/`.
- Motion: eased dolly push-ins, a dive-through-the-screen match cut, gold light-streak wipes, a 3D calendar page flip, a card fan reveal, depth-of-field blur, bokeh particles, film grain, and a vignette.
- Audio: original procedural score (D major, 96 BPM; chords change on the scene cuts) plus SFX (risers, whooshes, chimes, stamp thud, page flip). The music ducks under the voice through a side-chain.

## Rebuild

```bash
pip install numpy scipy piper-tts
# Voice model: piper "ar_JO-kareem-medium" (.onnx + .onnx.json, Arabic male)
VOICE_MODEL=/path/to/ar_JO-kareem-medium.onnx ./build.sh [workdir]
```

`scene.html?t=6.3` opens any moment for preview. Every animation is a pure function of `t`, so renders are deterministic.

## Suggested post caption

> هل تعلم أن الإيراد لا يُسجَّل بالضرورة عند استلام النقود؟
> مبدأ الاستحقاق يعني تسجيل الإيرادات عند تحققها والمصروفات عند نشوئها، بغض النظر عن موعد القبض أو الدفع.
> ببساطة، نسجل النشاط الاقتصادي وقت حدوثه، وليس وقت تحصيل أمواله.
>
> #محاسبة #مبدأ_الاستحقاق #القوائم_المالية #IFRS #Accounting #AccrualBasis
