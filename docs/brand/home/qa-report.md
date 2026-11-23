# OzarLand Home — QA Report

All checks below refer to the final delivered raster files. `P` means visually or technically passed; `N/A` means the check does not apply to that file. The numbered columns correspond, in order, to: 1 no embedded text; 2 approved LUMO/cast; 3 visible anatomy and held objects; 4 established hand-painted style; 5 palette and light; 6 framing and safe margins; 7 grayscale readability; 8 excluded content; 9 tile seam; 10 transparency and edge quality. Each file has its own result for all ten checks.

Final dimensions, formats, alpha flags and byte counts were read from the output files and recorded in `manifest-home.json`. Painted scenes and the social crop were converted to grayscale and visually inspected. Ornament and seal PNGs were composited on light and dark backgrounds; texture tiles and page mockups were also reviewed in grayscale. The three texture WebPs were assembled as decoded 2×2 mosaics; opposite edges are pixel-identical. The margin vine was additionally repeated vertically and checked for a continuous seam.

| File | Attempts | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Notes |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|
| `HOME-hero-great-book.webp` | 2 | P | P | P | P | P | P | P | P | N/A | N/A | Second pass added a distinct small brass belt key; all other approved composition details were retained. |
| `HOME-hero-great-book-mobile.webp` | 1 | P | P | P | P | P | P | P | P | N/A | N/A | Composed as a separate square scene rather than cropped from desktop. |
| `HOME-chapters-map.webp` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | N/A | Eight markers counted along one continuous path; no labels. |
| `HOME-community-scriptorium.webp` | 1 | P | P | P | P | P | P | P | P | N/A | N/A | Visible faces and hands are coherent at delivered scale; hands partly hidden by the map and held objects are not fully exposed. |
| `HOME-author-desk.webp` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | N/A | No people; book pages contain no legible writing. |
| `HOME-colophon.webp` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | N/A | Cropped to the exact banner ratio while keeping the book and blank spines visible. |
| `HOME-social-preview.jpg` | 1 | P | P | P | P | P | P | P | P | N/A | N/A | Derived from the final hero; JPEG quality was reduced to fit the 200 KB limit. |
| `HOME-parchment-tile.webp` | 1 | P | N/A | N/A | N/A | P | N/A | P | P | P | N/A | 2×2 decoded WebP mosaic has pixel-identical opposite edges; grain stays intentionally subtle. |
| `HOME-parchment-tile-dark.webp` | 1 | P | N/A | N/A | N/A | P | N/A | P | P | P | N/A | 2×2 decoded WebP mosaic has pixel-identical opposite edges; grain stays intentionally subtle. |
| `HOME-leather-tile.webp` | 1 | P | N/A | N/A | N/A | P | N/A | P | P | P | N/A | 2×2 decoded WebP mosaic has pixel-identical opposite edges. |
| `HOME-margin-border.png` | 3 | P | N/A | N/A | P | P | P | P | P | N/A | P | Third attempt selected. The narrow center stem intentionally meets top and bottom to repeat seamlessly; side ornament stays inside margins. |
| `HOME-divider.png` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | P | Checked over pale and dark backgrounds; no visible matte or halo. |
| `HOME-corner.png` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | P | One corner only; mirror for other positions. |
| `HOME-dropcap-frame.png` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | P | Central 256×256 area is fully transparent; initial remains HTML text. |
| `HOME-ribbon-bookmark.png` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | P | Visible ribbon tail is split; composited on light and dark grounds. |
| `HOME-seal-draft.png` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | P | Smooth surface distinguishes draft by form; checked in grayscale and on light/dark grounds. |
| `HOME-seal-lab-verified.png` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | P | Lantern relief remains identifiable in grayscale and on light/dark grounds. |
| `HOME-seal-validated.png` | 1 | P | N/A | N/A | P | P | P | P | P | N/A | P | Compass, brass ring and ribbon distinguish it in grayscale and on light/dark grounds. |
| `HOME-mockup-desktop.png` | 1 | P | N/A | N/A | N/A | P | P | P | P | N/A | N/A | Text is represented only by gray bars, as requested. |
| `HOME-mockup-mobile.png` | 1 | P | N/A | N/A | N/A | P | P | P | P | N/A | N/A | Text is represented only by gray bars, as requested. |
| `HOME-contact-sheet.png` | 1 | P | N/A | N/A | N/A | P | P | P | P | N/A | N/A | Reviewed at full size and as a grayscale version; sheet shows all 20 other image assets. |

## Decisions and remaining imperfections

- The desktop hero received two passes: the second made LUMO’s small brass belt key distinct while preserving the approved composition. The mobile hero was composed separately in a square frame. The map has eight unlabelled markers on one continuous route. Noor is shown using her wheelchair with her abacus in the community scene.
- The vertical vine took three passes; the final uses a continuous center stem touching the top and bottom edges so the requested vertical repeat has no break. Its leaves and brass details retain side margins.
- The colophon was cropped to the requested banner ratio while retaining the closed book and blank spines. The social preview is a centered crop of the final desktop hero. JPEG quality was tuned to keep it below 200 KB.
- The three textures were made as periodic, low-amplitude grain fields; their near-invisible texture is intentional.
- Some community-scene hands are partly obscured by the map and held objects. No visible face, hand, eye or object interaction shows an obvious anatomy fault at delivered size; obscured fingers cannot be independently inspected.
- No unresolved QA failures remain. No asset is marked `needs-review`.
