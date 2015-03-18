# Convert dia to dia / SVG
set(DESIGN_NOTES_DIAGRAMS_DIA
  opening_resource.dia
  execute_task.dia
)

foreach(dia ${DESIGN_NOTES_DIAGRAMS_DIA})
  dia2png( ${dia} )
  dia2svg( ${dia} )
endforeach()
