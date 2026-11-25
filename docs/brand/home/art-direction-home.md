# OzarLand Home — Art Direction

## Concept (five lines)
The homepage is the Grand Book of the island, kept open in a sunlit archive library.
Its pages hold practical knowledge passed between working OpenStack operators.
Leather, brass, ribbons, maps and chapter ornaments extend the existing island world.
LUMO appears as the calm, accomplished cartographer beside the book, never as an authority figure.
The book is a visual metaphor for accumulated experience; it does not certify technical correctness.

## Continuity and new direction
Carry forward the approved hand-painted anime fantasy treatment: clear blue sky, white clouds, turquoise sea, sunlit pale stone, terracotta roofs, timber terraces, green vines, brass details and small navy cloud pennants. Keep LUMO's approved adult proportions, auburn curls, patterned headband, goggles, cream shirt, navy cloud cape, compass brooch, leather satchel, brown trousers and lace-up boots. The homepage adds the archive library, a Mediterranean guild scriptorium, the open Great Book, leather binding, brass clasps, blank illuminated initials, wax seals and ribbon bookmarks. It extends the Academy's established eight-stop island journey without replacing it.

## Palette and contrast
The table defines every palette role. Contrast ratios use WCAG relative luminance calculations; ratios compare each named text or accent color against a solid background. Decorative accents are not approved for small text.

| Color | Hex | Role |
|---|---|---|
| Soft parchment | `#FBF4E4` | Light page background; dark-mode text |
| Surface | `#FFFDF8` | Cards and quiet panels |
| Parchment | `#F3E3C3` | Book pages and light-mode texture |
| Strong navy | `#152A50` | Main text; dark-mode background |
| Navy | `#1F3A6B` | Buttons, links, dark-mode raised surface |
| Wood / brass | `#C4904F` | Borders, hardware, ornament |
| Dark wood | `#6B4220` | Book leather, timber, linework |
| Lantern gold | `#F0B440` | Focus ring and local lantern glow |
| Sea | `#1E9FB5` | Sea and map water |
| Sky | `#2F6FD0` | Sky and map accents |
| Green | `#2C7A43` | Vines and island foliage |
| Terracotta | `#B55A3A` | Roofs and clay details |
| Violet | `#6E5A9E` | Minor map accent |
| Olive | `#5B7F2A` | Minor map accent |
| Added ink | `#2E291F` | Extra dark brown linework/ink only |
| Added wax | `#963D38` | Extra red-brown seal wax |

**Text pairings:** `#152A50` on `#FBF4E4` is **12.96:1**, on `#FFFDF8` **13.97:1**, and on `#F3E3C3` **11.22:1**. In dark mode, `#FBF4E4` text on `#152A50` is **12.96:1**; on raised `#1F3A6B` it is **10.22:1**. `#F3E3C3` on those dark surfaces is **11.22:1** and **8.84:1** respectively.

**Accent contrast on light `#FBF4E4` / dark `#152A50`:** brass `#C4904F` **2.57:1 / 5.04:1**; dark wood `#6B4220` **7.90:1 / 1.64:1**; lantern gold `#F0B440` **1.69:1 / 7.65:1**; sea `#1E9FB5` **2.87:1 / 4.52:1**; sky `#2F6FD0` **4.45:1 / 2.91:1**; green `#2C7A43` **4.82:1 / 2.69:1**; terracotta `#B55A3A` **4.27:1 / 3.03:1**; violet `#6E5A9E` **5.29:1 / 2.45:1**; olive `#5B7F2A` **4.25:1 / 3.05:1**; added ink `#2E291F` **13.19:1 / 1.02:1**; added wax `#963D38` **6.34:1 / 2.04:1**. Accent ratios below 4.5:1 are decorative only. Use navy for small links and controls in light mode and soft parchment for small copy in dark mode. The only added hues are ink and wax; existing dark wood supplies the leather shade.

## Typography
Use system fonts only. Headings: `Iowan Old Style`, `Palatino Linotype`, Palatino, Georgia, serif. Body, navigation and controls retain the site's current system sans-serif stack. Use a restrained initial-cap frame as decoration; place any actual initial in HTML. No blackletter or web fonts.

## Section treatment
1. Header: a leather-like navy book cover with the existing logo and five links (Academy, Runbooks, Book, Join in, About).
2. Opening: title “OzarLand”, promise, primary and secondary actions, plus a distinct “In an incident?” shortcut beside the Great Book illustration.
3. Academy: an eight-chapter table of contents paired with a parchment island map and continuous route: LUMO's village, Quick lab, Deployment patterns, Kolla-Ansible Academy, VM runbooks, Production guide, OKD OpenStack lab, Operator skills.
4. Trust: three text-labeled statuses with distinguishable wax forms: smooth unmarked draft; lantern-impressed lab-verified; compass-impressed, brass-ringed validated with ribbon.
5. The book and its author: a writing table and a concise author note, with the book as the main action.
6. Join in: three cards for the newcomer path, Discussions and a first contribution.
7. Footer: a quiet colophon with closed book and plain links.

The community scriptorium illustration is kept in `site/assets/home/` but no longer shown on the home page, which was shortened so that a visitor does not miss what matters.

## Ornaments and mobile use
The margin vine frames desktop text columns but stays outside the text measure; on mobile it is omitted or reduced to a short side flourish. The divider separates sections at desktop and becomes a short centered rule on mobile. The single corner ornament can be mirrored at page corners and reduced to one upper corner on mobile. The blank drop-cap frame is only a background for an HTML initial; omit it where it would crowd mobile copy. The ribbon bookmark can mark the active chapter on desktop and becomes a narrow top-edge tab on mobile. The three seal PNGs accompany text labels and remain small enough not to compete with them. No decorative illustration sits behind a paragraph; text panels use only a very faint parchment texture.

## Do / do not
**Do:** keep the library bright with late-morning light through arches; use soft painted shadows; keep the page and map marks blank or abstract; show LUMO calmly and consistently; give the other cast members equal space; depict Noor using her wheelchair naturally; check grayscale value hierarchy.

**Do not:** add readable text, numbers, fake lettering, logos, runes, watermarks or signatures to images; crop faces, hands, goggles, brooch, lantern or feet; add magic, menace, weapons, panic, religious symbols or science-fiction robots; make LUMO childish, omniscient or authoritative; place art behind body paragraphs; imply that the book itself proves a procedure correct.

## Metaphor limits
The book stands for knowledge recorded and shared. A page's appearance, ornament or status seal is not technical evidence. Only the site's explicit review process and supporting technical content can substantiate a procedure.
