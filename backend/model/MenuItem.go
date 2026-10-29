package model

import "time"

type MenuItem struct {
	Menu_item_id   int        `json:"menu_item_id"`
	Menu_item_name string     `json:"menu_item_name"`
	Price          float64    `json:"price"`
	ImageURL       string     `json:"image_url"`
	SeasonStart    *time.Time `json:"season_start"`
	SeasonEnd      *time.Time `json:"season_end"`
}

func (m MenuItem) InSeason(day time.Time) bool {
	return (m.SeasonStart == nil || !day.Before(*m.SeasonStart)) &&
		(m.SeasonEnd == nil || !day.After(*m.SeasonEnd))
}
