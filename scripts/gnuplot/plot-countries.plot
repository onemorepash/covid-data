set datafile separator ","

set style line 101 lc rgb '#808080' lt 1 lw 1
set border ls 101

set style line 1  linecolor rgb "#a6cee3"  linewidth 1.000 dashtype solid pointtype 7 pointsize 1
set style line 2  linecolor rgb "#fb9a99"  linewidth 1.000 dashtype solid pointtype 7 pointsize 1

#set style line 11  linecolor rgb "#808080"  linewidth 1.000 dashtype solid pointtype 1 pointsize default
#set style line 12  lt 0 linecolor rgb "#808080"  linewidth 1.000 dashtype 4 pointtype 0 pointsize default

set boxwidth 0.75 relative
set style fill solid 0.45 noborder

set term pngcairo size 1800,1200 font "Liberation Sans,12"

set output "../../plots/per-country/france.png"

filename = "../../data/worldmeters.info/france.txt"

set timefmt "%Y-%m-%d"

stats filename every ::1 u 2:5 nooutput prefix "DOC"
stats filename every ::1 u 2   nooutput prefix "CASES"
stats filename every ::1 u 5   nooutput prefix "DEATHS"


set multiplot layout 2,2 margin 0.1,0.95,0.1,0.85 spacing 0.1,0.1
set label 100 "France" center font ",40" at screen 0.5, 0.95 tc '#505050'


set xdata time

set xrange [:"2020-04-04"]

set yrange [0:50]

set format x "%b, %d" timedate
set format y "%.0f%%"
set format y2 "%.0s%c"

set ylabel "Daily growth rate\n\n" tc '#808080'
set y2label "Total deaths" tc '#808080'

set grid front

set ytics nomirror out 5
set y2tics nomirror out
set xtics nomirror out
set mytics

set key top left opaque tc '#808080'

plot filename every ::1 u 1:2 w boxes ls 1 axis x1y2 t "Total cases", \
     filename every ::1 u 1:(($3-1)*100) w points ls 1 lw 3 axis x1y1  notitle, \
     filename every ::1 u 1:(($3-1)*100) w l ls 1 dashtype 1 lw 3 s sb axis x1y1 notitle, \
     NaN w linespoints ls 1 lw 3 t "Daily growth rate"

set key top left opaque tc '#808080'
plot filename every ::1 u 1:5 w boxes ls 2 axis x1y2 t "Total deaths", \
     filename every ::1 u 1:(($6-1)*100) w points ls 2 lw 3 axis x1y1 notitle, \
     filename every ::1 u 1:(($6-1)*100) w lines ls 2 dashtype 1 lw 3 s sb axis x1y1 notitle, \
     NaN w linespoints ls 2 lw 3 t "Daily growth rate"


unset mytics
set ytics autofreq

set ylabel "New daily cases\n" tc '#808080'
set y2label "New daily deaths" tc '#808080

set key top left opaque tc '#808080'


unset yrange
unset y2range
set format y "%.0s%c"
set format y2 "%.0s%c"

#plot filename every ::1 u (timecolumn(1)-0.2*24*3600):4 w boxes ls 1 axis x1y1 t "New daily cases", \
#     filename every ::1 u (timecolumn(1)+0.2*24*3600):7 w boxes ls 2 axis x1y2 t "New daily deaths"

plot  filename every ::1 u 1:4 w points ls 1 lw 3 axis x1y1 notitle, \
      filename every ::1 u 1:4 w lines ls 1 lw 3 s sb axis x1y1 notitle, \
      NaN w linespoints ls 1 lw 3 axis x1y1 t "New daily cases", \
      filename every ::1 u 1:7 w point ls 2 lw 3 axis x1y2 notitle, \
      filename every ::1 u 1:7 w lines ls 2 lw 3 s sb axis x1y2 notitle, \
      NaN w linespoints ls 2 lw 3 axis x1y2 t "New daily deaths"

unset xdata
set format x "%.0s%c"
set format y "%.0s%c"
unset xrange
unset yrange
set yrange [0:]


set ylabel "Deaths\n" tc '#808080'
set xlabel "Cases" tc '#808080'
unset y2label

unset y2tics
set key top left opaque

set label 1 at (CASES_max-CASES_min)/2,DEATHS_max*0.85  sprintf("ρ = %.3f", DOC_correlation) left front enhanced tc '#808080'

set label 2 at (CASES_max-CASES_min)/2,DEATHS_max*0.78 sprintf("Mortality: %.1f%%", DEATHS_max/CASES_max*100) left front enhanced tc '#808080'



#set label 2 at (CASES_max-CASES_min)/2.5,DEATHS_max*0.72 sprintf("%.1f deaths per 1000 cases (linear fit)", DOC_slope*1000) right front enhanced


plot filename every ::1 u 2:5 w points ls 2 lw 3 axis x1y1 notitle, \
     filename every ::1 u 2:5 w lines ls 2 lw 2 s sb axis x1y1 t "Deaths over Cases", \
     DOC_slope*x + DOC_intercept w l ls 2 lw 1 dashtype 2 t "Linear fit"

unset multiplot
