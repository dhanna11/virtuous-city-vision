# TODO · Check the Arabic and Hebrew

Added 12 Oct 2026 at the author's request. Not started.

The slides carry a few lines of Arabic and Hebrew (identity A, `docs/design/`). They were written by AI. The author expects AI to be the main translator, so the plan is to make AI translation as reliable as it can be, then get one human pass on the cover if possible.

## What is on the slides

All of it is set in `tools/make-slides.py` (`AR_TITLE`, `HE_TITLE`, `AR_CITY`, `HE_CITY`, `AR_SAADA`, `HE_SAADA`).

| Where | English | Arabic | Hebrew | Status |
|---|---|---|---|---|
| Cover, telos divider | the Virtuous City | المدينة الفاضلة | העיר המעולה | **Confirmed.** Arabic is Al-Farabi's own phrase; Hebrew Wikipedia renders his book as דעותיהם של אנשי העיר המעולה (checked 12 Oct 2026). |
| Architecture slide (centre of the wheel) | happiness (sa'ada), the telos | السعادة | האושר | To check: is האושר the term used for Farabi's *sa'ada* in Hebrew scholarship? |
| Cover, under the title | Ending the October 7th Firestorm Must Restore Our Humanity | إنهاء العاصفة النارية للسابع من أكتوبر يجب أن يعيد إلينا إنسانيتنا | סיום סופת האש של השבעה באוקטובר חייב להשיב לנו את אנושיותנו | To check, most of all. |

"Firestorm" deliberately avoids each side's own name for 7 October (Hamas: طوفان الأقصى, "Al-Aqsa Flood"; Israelis often: השבת השחורה, "Black Sabbath"). Keep that neutrality; check that the literal "storm of fire" (العاصفة النارية / סופת האש) reads natively and not as translated.

## Steps

- [ ] **Back-translate.** Have a different model translate each Arabic and Hebrew line back into English; check that the meaning survived.
- [ ] **Cross-check models.** Ask two or three frontier models for their own renderings, independently. Where they agree, keep; where they differ, that phrase is the risk.
- [ ] **Alternatives with connotations.** For "firestorm" and for the title's register, ask for three renderings each and how they read to Palestinian, Gulf and Egyptian readers (Arabic) and to Israeli readers across the spectrum (Hebrew).
- [ ] **Fixed terms against sources.** Check السعادة / האושר for Farabi's *sa'ada* against scholarly translations or Wikipedia in each language, as was done for the Virtuous City.
- [ ] **One human pass, if possible.** One Arabic and one Hebrew speaker read the cover. Most viewers only see the cover.
- [ ] **Record the outcome.** Update the table above, change the constants in `tools/make-slides.py`, rebuild, and drop the "working translations" notes in `CLAUDE.md` and `docs/design/README.md` for whatever is confirmed.
- [ ] **Before adding any new Arabic or Hebrew,** add it to the table first.
