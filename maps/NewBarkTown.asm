	object_const_def
	const NEWBARKTOWN_POKEFAN_M

NewBarkTown_MapScripts:
	def_scene_scripts

	def_callbacks
	callback MAPCALLBACK_NEWMAP, .FlyPoint

.FlyPoint:
	setflag ENGINE_FLYPOINT_NEW_BARK
	clearevent EVENT_FIRST_TIME_BANKING_WITH_MOM
	endcallback

TrainerJorge:
	trainer POKEFANF, JORGE, EVENT_BEAT_POKEFANF_JORGE, TrainerJorgeSeenText, TrainerJorgeBeatenText, 0, .Script

.Script:
	endifjustbattled
	opentext
	writetext TrainerJorgeAfterBattleText
	waitbutton
	closetext
	end

TrainerJorgeSeenText:
	text "Come here"
	line "you sussy baka"
	done

TrainerJorgeBeatenText:
	text "sus"
	done

TrainerJorgeAfterBattleText:
	text "Lmao get rekt"
	line "noob"
	done


NewBarkTown_MapEvents:
	db 0, 0 ; filler

	def_warp_events
	warp_event 15,  7, PLAYERS_HOUSE_1F, 1
	warp_event  3,  7, BATTLE_TOWER_OUTSIDE, 1
	warp_event  9,  3, INDIGO_PLATEAU_POKECENTER_1F, 1

	def_coord_events

	def_bg_events

	def_object_events
	; object_event 10, 10, SPRITE_POKEFAN_M, SPRITEMOVEDATA_STANDING_DOWN, 0, 0, -1, -1, PAL_NPC_GREEN, OBJECTTYPE_TRAINER, 1, TrainerJorge, -1
