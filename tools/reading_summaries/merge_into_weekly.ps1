# Insert reading-summary slides into a weekly deck's "Papers to Read" section, then export the PDF.
#
#   powershell -File merge_into_weekly.ps1 -Weekly <weekly.pptx> -Summary <paper-slides.pptx> -After <slideNo> [-NoPdf]
#
# <paper-slides.pptx> comes from: node build_readings_deck.js <json> <week> <title> <out> <start> <total>
# The section footers already in the weekly deck ("k / old") are renumbered to the new total, and their
# progress bars are resized. Run it once per deck: on an already-merged deck it would insert again.
param([string]$Weekly, [string]$Summary, [int]$After, [switch]$NoPdf)

$Weekly = (Resolve-Path $Weekly).Path
$Summary = (Resolve-Path $Summary).Path
$ppt = New-Object -ComObject PowerPoint.Application
$p = $ppt.Presentations.Open($Weekly, $false, $false, $false)

# The section starts at its divider; find it by walking back from $After to the slide without "k / n".
function Get-Counter($slide) {
  foreach ($sh in $slide.Shapes) {
    if ($sh.HasTextFrame -and $sh.TextFrame.TextRange.Text -match '^\s*(\d+) / (\d+)\s*$') { return $sh }
  }
  return $null
}

$s = $p.Slides.Item($After)
$label = $null
foreach ($sh in $s.Shapes) {
  if ($sh.HasTextFrame -and $sh.TextFrame.TextRange.Text -like 'DS 501 *') { $label = $sh.TextFrame.TextRange.Text }
}
$c = Get-Counter $s
$null = $c.TextFrame.TextRange.Text -match '(\d+) / (\d+)'
$oldTotal = [int]$Matches[2]
$first = $After - [int]$Matches[1] + 1          # first slide of the section (the divider)
$oldLast = $first + $oldTotal - 1

$before = $p.Slides.Count
$null = $p.Slides.InsertFromFile($Summary, $After)
$added = $p.Slides.Count - $before
$newTotal = $oldTotal + $added
$newLast = $oldLast + $added

$red = 0xC8 + 0x10 * 256 + 0x2E * 65536          # C8102E as an Office BGR integer
$slideW = $p.PageSetup.SlideWidth
foreach ($i in @($first..$After) + @(($After + $added + 1)..$newLast)) {
  $sl = $p.Slides.Item($i)
  $c = Get-Counter $sl
  if ($c -eq $null) { continue }
  $null = $c.TextFrame.TextRange.Text -match '(\d+) / (\d+)'
  $k = [int]$Matches[1]
  if ($i -gt $After) { $k += $added }
  $c.TextFrame.TextRange.Text = "$k / $newTotal"
  foreach ($sh in $sl.Shapes) {
    if ($sh.Top -gt 530 -and $sh.Height -lt 8 -and $sh.Fill.ForeColor.RGB -eq $red) { $sh.Width = $slideW * $k / $newTotal }
  }
}

$p.Save()
if (-not $NoPdf) { $p.SaveAs([System.IO.Path]::ChangeExtension($Weekly, ".pdf"), 32) }
$p.Close()
$ppt.Quit()
"Inserted $added slides after slide $After; section '$label' is now $newTotal slides (slides $first-$newLast)."
