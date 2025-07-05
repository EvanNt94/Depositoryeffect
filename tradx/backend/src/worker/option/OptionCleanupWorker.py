"""DELETE FROM option.options WHERE expiry < CURRENT_DATE;
DELETE FROM option.option_prices WHERE option_id NOT IN (SELECT id FROM option.options);
DELETE FROM option.option_greeks WHERE option_id NOT IN (SELECT id FROM option.options);

    1.	Ja, lösche expired Options regelmäßig
	2.	Starte mit DELETE FROM option.options WHERE expiry < CURRENT_DATE
	3.	Ergänze CASCADE DELETE in option_prices und option_greeks, wenn noch nicht gesetzt
	4.	Später → Archivstruktur bauen (sobald dein Bot produktiv läuft)
"""