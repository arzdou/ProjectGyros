	db TALONFLAME

	db 78, 81, 71, 69, 74, 126, 
	;   hp  atk  def  spd  sat  sdf

	db FIRE, FLYING ; type
	db 45 ; catch rate
	db 175 ; base exp
	db NO_ITEM, NO_ITEM ; items
	db GENDER_F50 ; gender ratio
	db 100 ; unkown 1
	db 15 ; step cycles to hatch
	db 5 ; unkown 2
	INCBIN "gfx/pokemon/talonflame/front.dimensions"
	dw NULL, NULL ; unused (beta front/back pics)
	db GROWTH_MEDIUM_SLOW ; growth rate
	dn EGG_FLYING, EGG_FLYING ; egg groups

	; tm/hm learnset
	tmhm HYPER_BEAM, TOXIC, DOUBLE_TEAM, FIRE_BLAST, SWIFT, REST, THIEF, SNORE, PROTECT, ENDURE, SWAGGER, ATTRACT, SLEEP_TALK, RETURN, FRUSTRATION, HIDDEN_POWER, SUNNY_DAY
	; end
