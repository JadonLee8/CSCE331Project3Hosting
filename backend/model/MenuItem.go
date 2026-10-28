package model

import "time"

type MenuItem struct {
	MenuItemID  int
	Name        string
	Price       float64
	ImageURL    string
	SeasonStart *time.Time
	SeasonEnd   *time.Time
}

func (m MenuItem) InSeason(day time.Time) bool {
	return (m.SeasonStart == nil || !day.Before(*m.SeasonStart)) &&
		(m.SeasonEnd == nil || !day.After(*m.SeasonEnd))
}
