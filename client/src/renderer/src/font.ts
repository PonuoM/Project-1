/**
 * The chosen Thai pixel font goes at public/fonts/GameFont.ttf. Relative URL so it works from both the dev
 * server and the packaged file:// build. Canvas text needs it loaded before first use.
 */
export async function loadGameFont(): Promise<void> {
  try {
    const face = new FontFace('GameFont', 'url(fonts/GameFont.ttf)')
    document.fonts.add(await face.load())
  } catch {
    /* no font file yet: the fallback fonts are fine */
  }
}
