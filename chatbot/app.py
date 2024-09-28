from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Predefined remedies data
remedies_data = {
    
  "Sore Throat": {
    "remedy": "Salt Water Gargle, Honey, Marshmallow Root Tea",
    "preparation": "Dissolve 1/4 to 1/2 teaspoon of salt in warm water and gargle for 30 seconds. Honey can be taken directly by the spoonful or added to warm tea. For marshmallow root tea, steep a teaspoon of dried marshmallow root in a cup of boiling water for 10 minutes, strain, and sip slowly.",
    "use": "Saltwater reduces swelling in the throat, honey soothes irritation, and marshmallow root creates a protective coating in the throat to reduce discomfort."
  },
  "Constipation": {
    "remedy": "Prunes, Flaxseed, Psyllium Husk",
    "preparation": "Eat a handful (5-7) of prunes or drink prune juice. Flaxseed should be ground and added to smoothies, oatmeal, or yogurt. For psyllium husk, mix 1 tablespoon in a glass of water and drink it immediately, followed by another glass of water.",
    "use": "Prunes help soften stools, flaxseed adds fiber, and psyllium husk promotes bowel movement by absorbing water in the gut."
  },
  "Nausea": {
    "remedy": "Ginger, Lemon, Peppermint",
    "preparation": "To make ginger tea, slice a piece of fresh ginger and boil in water for 10 minutes, then strain and drink. Lemon can be sliced and added to warm water for a refreshing drink. Peppermint tea is made by steeping a handful of fresh or dried peppermint leaves in hot water for 5-10 minutes.",
    "use": "Ginger calms the stomach, lemon refreshes and neutralizes acid, and peppermint soothes nausea."
  },
  "Indigestion": {
    "remedy": "Baking Soda, Lemon Juice, Fennel",
    "preparation": "Mix 1/2 teaspoon of baking soda in a glass of water and drink it. For lemon juice, squeeze half a lemon into warm water and drink before meals. Fennel seeds can be chewed after meals or brewed into tea by steeping a teaspoon of seeds in hot water for 10 minutes.",
    "use": "Baking soda neutralizes stomach acid, lemon juice aids digestion, and fennel reduces bloating and discomfort."
  },
  "Cough": {
    "remedy": "Honey, Thyme, Licorice Root",
    "preparation": "Take a spoonful of honey directly or mix it into warm tea. Thyme tea is made by steeping a tablespoon of dried thyme in boiling water for 10 minutes, then straining and drinking. Licorice root tea can be prepared by simmering 1-2 teaspoons of dried root in water for 10 minutes, then straining.",
    "use": "Honey soothes the throat, thyme works as an expectorant, and licorice root calms irritated airways."
  },
  "Menstrual Cramps": {
    "remedy": "Ginger, Cinnamon, Heat Therapy",
    "preparation": "Ginger and cinnamon can be boiled together in water for 10 minutes to make tea. For heat therapy, apply a hot water bottle or heating pad to your lower abdomen for 20-30 minutes.",
    "use": "Ginger and cinnamon reduce pain by lowering inflammation, and heat relaxes the muscles, relieving cramps."
  },
  "Cold Sores": {
    "remedy": "Lemon Balm, Licorice Root, Aloe Vera",
    "preparation": "Apply lemon balm cream or oil directly to the cold sore several times a day. Licorice root extract or cream can also be applied topically. For aloe vera, apply fresh gel from the plant to the cold sore and leave it on until it dries.",
    "use": "Lemon balm and licorice root speed healing, while aloe vera soothes the area and reduces inflammation."
  },
  "Ear Infection": {
    "remedy": "Garlic Oil, Mullein Oil, Warm Compress",
    "preparation": "Warm garlic oil slightly and put a few drops into the affected ear. Mullein oil can be applied in the same way. To use a warm compress, soak a clean cloth in hot water, wring it out, and place it over the ear for 10-15 minutes.",
    "use": "Garlic oil has antimicrobial properties, mullein oil reduces swelling, and a warm compress eases pain."
  },
  "Bad Breath": {
    "remedy": "Parsley, Fennel Seeds, Baking Soda",
    "preparation": "Chew a few fresh parsley leaves after meals to freshen your breath. Fennel seeds can also be chewed or brewed into tea by steeping a teaspoon in boiling water for 10 minutes. Baking soda can be mixed with water to use as a mouth rinse.",
    "use": "Parsley and fennel naturally freshen breath, while baking soda neutralizes bad odors."
  },
  "Bloating": {
    "remedy": "Peppermint, Dandelion Tea, Activated Charcoal",
    "preparation": "Brew peppermint tea by steeping fresh or dried leaves in hot water for 5-10 minutes. Dandelion tea can be made by steeping dried dandelion root in boiling water for 10-15 minutes. Activated charcoal supplements are taken as directed on the package.",
    "use": "Peppermint relaxes digestive muscles, dandelion tea acts as a natural diuretic, and activated charcoal absorbs excess gas."
  },
  "Diarrhea": {
    "remedy": "Bananas, Probiotics, Chamomile",
    "preparation": "Eat ripe bananas to help firm up stools. Probiotics can be taken in supplement form or through yogurt with live cultures. For chamomile tea, steep a tablespoon of dried chamomile flowers in hot water for 10 minutes.",
    "use": "Bananas help restore normal bowel function, probiotics replenish healthy gut bacteria, and chamomile calms the digestive system."
  },
  "Sunburn": {
    "remedy": "Aloe Vera, Cucumber, Oatmeal Bath",
    "preparation": "Apply fresh aloe vera gel directly to the affected areas several times a day. Cucumber slices can be placed on the skin for cooling relief. To make an oatmeal bath, grind a cup of oats into a fine powder and add it to a lukewarm bath, soaking for 15-20 minutes.",
    "use": "Aloe vera cools the skin and promotes healing, cucumber reduces inflammation, and oatmeal soothes itching."
  },
  "Cholesterol": {
    "remedy": "Oats, Garlic, Green Tea",
    "preparation": "Cook oats as a breakfast porridge or add them to smoothies. Garlic can be eaten raw or taken as a supplement. Green tea is brewed by steeping tea leaves in hot water for 3-5 minutes.",
    "use": "Oats help lower bad cholesterol levels, garlic improves circulation, and green tea boosts overall heart health."
  },
  "Hair Loss": {
    "remedy": "Rosemary Oil, Aloe Vera, Biotin",
    "preparation": "Mix a few drops of rosemary oil with a carrier oil (like coconut oil) and massage into the scalp for 5-10 minutes before washing. Apply fresh aloe vera gel to the scalp and let it sit for 30 minutes before rinsing. Biotin supplements are taken as directed on the package.",
    "use": "Rosemary oil stimulates hair growth, aloe vera strengthens hair, and biotin supports hair and nail health."
  },
  "Body Odor": {
    "remedy": "Apple Cider Vinegar, Lemon Juice, Baking Soda",
    "preparation": "Dab apple cider vinegar or lemon juice onto underarms with a cotton ball. Baking soda can be mixed with a little water to form a paste and applied to underarms as a natural deodorant.",
    "use": "Apple cider vinegar and lemon juice kill bacteria that cause odor, while baking soda neutralizes odors naturally."
  },
  "Hemorrhoids": {
    "remedy": "Witch Hazel, Aloe Vera, Epsom Salt",
    "preparation": "Apply witch hazel directly to hemorrhoids using a cotton ball or pad. Aloe vera gel can be applied to soothe the area. For an Epsom salt bath, dissolve 1/2 cup of Epsom salt in warm water and soak for 15-20 minutes.",
    "use": "Witch hazel reduces inflammation and itching, aloe vera soothes irritation, and Epsom salt eases discomfort."
  },
  "Insect Bites": {
    "remedy": "Lavender Oil, Baking Soda, Calendula",
    "preparation": "Dilute a few drops of lavender oil in a carrier oil and apply it to insect bites. For baking soda, mix it with water to make a paste and apply it to the bite. Calendula can be used as a cream or salve applied directly to the skin.",
    "use": "Lavender oil reduces itching, baking soda neutralizes the venom, and calendula promotes healing."
  },
  "Dry Skin": {
    "remedy": "Coconut Oil, Shea Butter, Oatmeal Bath",
    "preparation": "Apply coconut oil or shea butter directly to the skin after a shower when the skin is still damp. For an oatmeal bath, grind a cup of oats into a fine powder and add it to lukewarm water, soaking for 15-20 minutes.",
    "use": "Coconut oil and shea butter moisturize the skin, while oatmeal soothes and hydrates dry skin."
  },
  "Fatigue": {
    "remedy": "Ginseng, Ashwagandha, Green Tea",
    "preparation": "Ginseng can be taken as a supplement or brewed as a tea by steeping the root in hot water. Ashwagandha is available in capsule form or as a powder to mix into drinks. Green tea is brewed by steeping tea leaves in hot water for 3-5 minutes.",
    "use": "Ginseng boosts energy levels, ashwagandha helps manage stress, and green tea provides a mild caffeine boost."
  },
  "Allergies": {
    "remedy": "Quercetin, Butterbur, Neti Pot",
    "preparation": "Quercetin is available as a supplement and should be taken as directed. Butterbur can also be taken in capsule form. A neti pot can be used with a saline solution to rinse nasal passages.",
    "use": "Quercetin and butterbur reduce histamine release, while a neti pot helps clear allergens from the nasal passages."
  },
  "Anxiety": {
    "remedy": "Chamomile Tea, Lavender Oil, Ashwagandha",
    "preparation": "Brew chamomile tea by steeping dried flowers in hot water for 5-10 minutes. Lavender oil can be diffused or applied topically. Ashwagandha supplements can be taken as directed.",
    "use": "Chamomile and lavender promote relaxation, while ashwagandha helps manage stress levels."
  },
  "Insomnia": {
    "remedy": "Valerian Root, Melatonin, Lavender",
    "preparation": "Valerian root can be taken as a supplement or brewed into tea. Melatonin is available as a supplement to be taken 30 minutes before bedtime. Lavender oil can be used in a diffuser or applied to pillows.",
    "use": "Valerian root promotes sleep, melatonin regulates sleep-wake cycles, and lavender induces relaxation."
  },
  "Nasal Congestion": {
    "remedy": "Eucalyptus Oil, Steam Inhalation, Saline Spray",
    "preparation": "Eucalyptus oil can be added to a diffuser or diluted in a carrier oil for topical use. For steam inhalation, add a few drops of eucalyptus oil to a bowl of hot water and inhale the steam. Saline spray can be used as directed.",
    "use": "Eucalyptus oil opens airways, steam clears mucus, and saline spray hydrates nasal passages."
  },
  "High Blood Pressure": {
    "remedy": "Garlic, Omega-3 Fatty Acids, Dark Chocolate",
    "preparation": "Garlic can be consumed raw or in supplement form. Omega-3s can be found in fish oil supplements or fatty fish. Dark chocolate should be 70% cocoa or higher and can be consumed in moderation.",
    "use": "Garlic helps lower blood pressure, omega-3s improve heart health, and dark chocolate may help improve circulation."
  },
  "Heartburn": {
    "remedy": "Ginger, Aloe Vera Juice, Apple Cider Vinegar",
    "preparation": "Ginger can be consumed as tea made by boiling fresh ginger in water. Aloe vera juice can be taken directly. Apple cider vinegar should be diluted with water before drinking.",
    "use": "Ginger reduces inflammation, aloe vera soothes the digestive tract, and apple cider vinegar aids digestion."
  },
  "Puffy Eyes": {
    "remedy": "Cold Compress, Cucumber Slices, Tea Bags",
    "preparation": "Apply a cold compress for 10-15 minutes. Cucumber slices can be placed on the eyes for 10 minutes. For tea bags, steep them in hot water, cool them in the fridge, and then place them on your eyes.",
    "use": "Cold compresses reduce swelling, cucumbers provide hydration, and tea bags contain tannins that reduce puffiness."
  }
  ,
  "Toothache": {
    "remedy": "Clove Oil, Salt Water Rinse, Garlic",
    "preparation": "Apply a drop of clove oil to the painful tooth with a cotton swab. For a saltwater rinse, dissolve 1/2 teaspoon of salt in warm water and swish it in your mouth for 30 seconds. Chew on a fresh garlic clove or apply crushed garlic directly to the affected area for pain relief.",
    "use": "Clove oil numbs the pain, salt water cleans the area and reduces inflammation, and garlic acts as a natural antibiotic."
  },
  "Acne": {
    "remedy": "Tea Tree Oil, Aloe Vera, Honey",
    "preparation": "Dilute a few drops of tea tree oil in a carrier oil (like coconut or jojoba oil) and apply it to the affected area with a cotton swab. Apply fresh aloe vera gel directly to acne spots. Honey can be applied as a mask by spreading a thin layer over the face, leaving it on for 10-15 minutes, and then rinsing with warm water.",
    "use": "Tea tree oil kills bacteria, aloe vera soothes the skin, and honey is antibacterial, helping to clear acne."
  },
  "Back Pain": {
    "remedy": "Ginger, Epsom Salt, Heat Therapy",
    "preparation": "Make ginger tea by boiling fresh ginger slices in water for 10 minutes, then strain and drink. For an Epsom salt bath, dissolve 2 cups of Epsom salt in warm water and soak for 20 minutes. Use a heating pad or hot water bottle on the sore area for 15-20 minutes.",
    "use": "Ginger reduces inflammation, Epsom salt relaxes muscles, and heat increases blood flow, which eases pain."
  },
  "Dandruff": {
    "remedy": "Apple Cider Vinegar, Coconut Oil, Tea Tree Oil",
    "preparation": "Mix equal parts apple cider vinegar and water and apply it to the scalp for 10-15 minutes before rinsing. Massage coconut oil into the scalp and leave it on for 30 minutes before washing. Add a few drops of tea tree oil to your shampoo and wash your hair as usual.",
    "use": "Apple cider vinegar restores the scalp's pH balance, coconut oil moisturizes, and tea tree oil fights fungus that causes dandruff."
  },
  "Motion Sickness": {
    "remedy": "Ginger, Peppermint, Acupressure",
    "preparation": "Chew on a small piece of fresh ginger or drink ginger tea (made by boiling fresh ginger in water for 10 minutes). Peppermint can be taken as tea by steeping leaves in hot water or inhaling peppermint essential oil. For acupressure, apply pressure to the inner wrist (three fingers width from the base of the hand) to relieve nausea.",
    "use": "Ginger calms the stomach, peppermint soothes nausea, and acupressure helps reduce the symptoms of motion sickness."
  },
  "Wound Healing": {
    "remedy": "Honey, Aloe Vera, Turmeric",
    "preparation": "Apply a thin layer of honey directly to the wound and cover it with a bandage. Aloe vera gel from the plant can be applied directly to the wound. Mix turmeric powder with water to make a paste and apply it to the wound, then cover with a bandage.",
    "use": "Honey promotes healing by keeping the wound moist and killing bacteria, aloe vera soothes the area, and turmeric reduces inflammation and speeds up healing."
  },
  "Varicose Veins": {
    "remedy": "Horse Chestnut, Witch Hazel, Compression",
    "preparation": "Horse chestnut extract can be applied topically to the veins or taken as a supplement. Apply witch hazel to the affected areas with a cotton ball. Wear compression stockings to improve circulation in the legs.",
    "use": "Horse chestnut strengthens vein walls, witch hazel reduces swelling, and compression stockings improve blood flow."
  },
  "Cuts and Scrapes": {
    "remedy": "Tea Tree Oil, Honey, Calendula",
    "preparation": "Dilute tea tree oil in a carrier oil and apply to the cut with a cotton swab. Apply a thin layer of honey directly to the wound and cover with a bandage. Calendula cream or ointment can be applied to the wound several times a day.",
    "use": "Tea tree oil kills bacteria, honey promotes healing, and calendula soothes and heals the skin."
  },
  "Liver Health": {
    "remedy": "Milk Thistle, Dandelion, Turmeric",
    "preparation": "Milk thistle can be taken as a supplement or brewed as tea by steeping a teaspoon of the seeds in hot water for 10 minutes. Dandelion root tea is made by simmering the dried root in water for 10-15 minutes. Turmeric can be added to meals or taken as a supplement.",
    "use": "Milk thistle protects liver cells, dandelion detoxifies the liver, and turmeric reduces inflammation."
  },
  "Colds": {
    "remedy": "Echinacea, Elderberry, Garlic",
    "preparation": "Echinacea can be taken as a supplement or tea by steeping dried echinacea in hot water for 10 minutes. Elderberry syrup is available at health stores, or you can make tea from dried berries. Garlic can be eaten raw or cooked, or taken as a supplement.",
    "use": "Echinacea boosts the immune system, elderberry fights viruses, and garlic has antiviral properties."
  },
  "Sore Muscles": {
    "remedy": "Epsom Salt, Arnica, Heat Therapy",
    "preparation": "Dissolve 2 cups of Epsom salt in a warm bath and soak for 20 minutes. Arnica gel or cream can be applied directly to the sore muscles. Use a heating pad or hot water bottle on the sore area for 15-20 minutes.",
    "use": "Epsom salt relaxes muscles, arnica reduces swelling and pain, and heat improves blood circulation to relieve soreness."
  },
  "Heart Palpitations": {
    "remedy": "Magnesium, Hawthorn Berry, Deep Breathing",
    "preparation": "Take magnesium as a supplement, or increase intake by eating foods like spinach, almonds, and avocados. Hawthorn berry can be taken as a supplement or brewed into tea by steeping dried berries in hot water for 10 minutes. Practice deep breathing by inhaling deeply through the nose and exhaling slowly through the mouth for several minutes.",
    "use": "Magnesium calms the heart, hawthorn berry supports heart function, and deep breathing reduces stress and palpitations."
  },
  "High Cholesterol": {
    "remedy": "Oats, Garlic, Green Tea",
    "preparation": "Cook oats as a breakfast porridge or add to smoothies. Garlic can be eaten raw or taken as a supplement. Green tea is brewed by steeping tea leaves in hot water for 3-5 minutes.",
    "use": "Oats help lower bad cholesterol, garlic improves blood circulation, and green tea enhances heart health."
  },
  "Memory and Focus": {
    "remedy": "Ginkgo Biloba, Rosemary, Omega-3",
    "preparation": "Ginkgo biloba can be taken as a supplement or brewed as tea. Rosemary essential oil can be diffused or applied to the wrists and temples. Omega-3 is found in fish oil supplements or foods like walnuts and flaxseeds.",
    "use": "Ginkgo biloba improves blood flow to the brain, rosemary enhances memory, and Omega-3 supports cognitive function."
  },
  "Menstrual Cramps": {
    "remedy": "Ginger, Cinnamon, Heat Therapy",
    "preparation": "Make ginger tea by boiling fresh ginger slices in water for 10 minutes, then strain and drink. Add 1/2 teaspoon of cinnamon powder to warm water or tea and drink. For heat therapy, use a heating pad or hot water bottle on the lower abdomen for 15-20 minutes.",
    "use": "Ginger reduces pain and inflammation, cinnamon helps ease cramps, and heat therapy relaxes muscles."
  },
  "Constipation": {
    "remedy": "Flaxseeds, Prune Juice, Psyllium Husk",
    "preparation": "Add ground flaxseeds to smoothies, oatmeal, or yogurt. Drink 1/2 to 1 cup of prune juice in the morning. Mix 1 tablespoon of psyllium husk in a glass of water or juice and drink immediately.",
    "use": "Flaxseeds and psyllium husk are rich in fiber, promoting bowel movements, while prune juice acts as a natural laxative."
  },
  "Low Energy": {
    "remedy": "Ashwagandha, Ginseng, B Vitamins",
    "preparation": "Take Ashwagandha in supplement form, following package instructions. Ginseng can be consumed as a supplement or brewed into tea by simmering the root in water for 10-15 minutes. B vitamins can be taken as a supplement or consumed through foods like eggs, leafy greens, and whole grains.",
    "use": "Ashwagandha reduces stress, ginseng boosts energy, and B vitamins support energy metabolism."
  },
  "Bloating": {
    "remedy": "Fennel Seeds, Peppermint Tea, Ginger",
    "preparation": "Chew on a teaspoon of fennel seeds after meals. Brew peppermint tea by steeping leaves in hot water for 5-10 minutes. Make ginger tea by boiling fresh ginger slices in water for 10 minutes.",
    "use": "Fennel seeds aid digestion, peppermint soothes the stomach, and ginger reduces gas and bloating."
  },
  "Allergies": {
    "remedy": "Local Honey, Quercetin, Neti Pot",
    "preparation": "Consume a teaspoon of local honey daily to build immunity to local pollen. Quercetin can be taken as a supplement or found in foods like onions and apples. Use a neti pot with saline solution to rinse the nasal passages.",
    "use": "Honey helps reduce allergy symptoms, quercetin acts as a natural antihistamine, and the neti pot clears nasal congestion."
  },
  "Fatigue": {
    "remedy": "Maca Root, Rhodiola, Sleep Hygiene",
    "preparation": "Take maca root as a supplement or mix powder into smoothies. Rhodiola can be taken as a supplement following package instructions. Practice sleep hygiene by maintaining a consistent sleep schedule and creating a relaxing bedtime routine.",
    "use": "Maca root increases energy levels, rhodiola combats fatigue, and sleep hygiene improves overall rest."
  },
  "Stress": {
    "remedy": "Lavender, Chamomile, Meditation",
    "preparation": "Use lavender essential oil in a diffuser or apply diluted oil to the wrists. Brew chamomile tea by steeping flowers in hot water for 5-10 minutes. Practice meditation by finding a quiet space and focusing on your breath for a few minutes.",
    "use": "Lavender calms the nervous system, chamomile promotes relaxation, and meditation reduces stress levels."
  },
  "Skin Irritation": {
    "remedy": "Aloe Vera, Coconut Oil, Oatmeal",
    "preparation": "Apply fresh aloe vera gel directly to the irritated skin. Massage coconut oil into the affected area. For an oatmeal bath, grind oatmeal into a fine powder and add it to warm bathwater.",
    "use": "Aloe vera soothes inflammation, coconut oil moisturizes, and oatmeal relieves itchiness."
  },
  "Heartburn": {
    "remedy": "Apple Cider Vinegar, Baking Soda, Ginger",
    "preparation": "Mix 1-2 tablespoons of apple cider vinegar in a glass of water and drink before meals. Mix 1/2 teaspoon of baking soda in water and drink for relief. Make ginger tea by boiling fresh ginger in water for 10 minutes.",
    "use": "Apple cider vinegar balances stomach acidity, baking soda neutralizes acid, and ginger soothes the digestive tract."
  },
  "Dry Skin": {
    "remedy": "Coconut Oil, Honey, Oatmeal",
    "preparation": "Apply coconut oil directly to dry areas of the skin. Mix honey with water for a moisturizing mask, leave it on for 15 minutes, then rinse. For an oatmeal bath, grind oatmeal into a fine powder and add it to warm bathwater.",
    "use": "Coconut oil provides moisture, honey hydrates, and oatmeal soothes and protects the skin."
  },
  "Indigestion": {
    "remedy": "Ginger, Peppermint, Apple Cider Vinegar",
    "preparation": "Make ginger tea by boiling fresh ginger slices in water for 10 minutes. Brew peppermint tea by steeping peppermint leaves in hot water for 5-10 minutes. Mix 1-2 tablespoons of apple cider vinegar in a glass of water and drink before meals.",
    "use": "Ginger aids digestion, peppermint relaxes the digestive tract, and apple cider vinegar helps balance stomach acidity."
  },
  "Ear Infections": {
    "remedy": "Garlic Oil, Warm Compress, Apple Cider Vinegar",
    "preparation": "Make garlic oil by heating minced garlic in olive oil, then strain and apply a few drops to the affected ear. Use a warm compress by soaking a cloth in warm water, wringing it out, and applying it to the ear. Mix equal parts of apple cider vinegar and water and use it as ear drops.",
    "use": "Garlic has antibacterial properties, warm compresses relieve pain, and apple cider vinegar helps restore pH balance."
  },
  "Fever": {
    "remedy": "Ginger Tea, Basil Leaves, Apple Cider Vinegar",
    "preparation": "Boil a few slices of ginger in water to make tea and drink 2-3 times a day. Chew 4-5 fresh basil leaves or boil them in water and sip. Mix 1 tablespoon of apple cider vinegar in a glass of water and drink it.",
    "use": "Ginger tea reduces body temperature, basil has antibacterial properties, and apple cider vinegar promotes sweating to reduce fever."
  },
"Oil Face": {
    "remedy": "Aloe Vera, Honey, Tea Tree Oil",
    "preparation": "Apply fresh aloe vera gel on the face, leave it for 10-15 minutes, and rinse. Mix 1 tablespoon of honey with a few drops of tea tree oil, apply as a mask, and leave for 20 minutes before rinsing.",
    "use": "Aloe vera controls oil production, honey moisturizes without making skin oily, and tea tree oil has antibacterial properties to prevent acne."
  },
"Cold": {
    "remedy": "Honey, Lemon, Garlic",
    "preparation": "Mix 1 tablespoon of honey with a few drops of lemon juice and warm water, and drink. Crush 2-3 garlic cloves and eat them raw or add them to soups.",
    "use": "Honey soothes the throat, lemon boosts immunity, and garlic has antiviral properties to reduce cold symptoms."
  },
"Weight Gain": {
    "remedy": "Peanut Butter, Milk, Bananas",
    "preparation": "Eat peanut butter with bread or in smoothies. Drink full-fat milk 2-3 times a day. Eat ripe bananas or blend them into smoothies.",
    "use": "Peanut butter is rich in healthy fats and calories, milk provides protein and nutrients, and bananas are calorie-dense and help with weight gain."
  },
"Weight Loss": {
    "remedy": "Green Tea, Lemon Water, Cinnamon",
    "preparation": "Brew green tea and drink 2-3 cups a day. Squeeze half a lemon into a glass of warm water and drink in the morning. Add 1 teaspoon of cinnamon powder to warm water or tea and drink daily.",
    "use": "Green tea boosts metabolism, lemon water aids digestion, and cinnamon regulates blood sugar and reduces cravings."
  },
  "High Blood Pressure": {
    "remedy": "Garlic, Banana, Flaxseeds",
    "preparation": "Crush 1-2 cloves of raw garlic and consume it with water daily. Eat a banana every day as part of your diet. Add 1 tablespoon of flaxseeds to your smoothies, yogurt, or salads.",
    "use": "Garlic helps relax blood vessels and reduce pressure, bananas are rich in potassium which helps balance sodium levels, and flaxseeds contain omega-3 fatty acids that lower blood pressure."
  },
"Low Blood Pressure": {
    "remedy": "Salt Water, Raisins, Coffee",
    "preparation": "Mix 1/2 teaspoon of salt in a glass of water and drink when you feel lightheaded. Soak 7-10 raisins in water overnight and eat them on an empty stomach in the morning. Drink a cup of strong coffee if you're experiencing low blood pressure symptoms.",
    "use": "Salt increases sodium levels in the body, raisins support adrenal function to normalize blood pressure, and coffee temporarily boosts blood pressure by stimulating the heart."
  },
  "Sugar": {
    "remedy": "Cinnamon, Fenugreek Seeds, Bitter Gourd",
    "preparation": "Add 1/2 teaspoon of cinnamon powder to your tea or smoothies daily. Soak 1 tablespoon of fenugreek seeds in water overnight and drink the water in the morning. Drink fresh bitter gourd juice or include it in your meals.",
    "use": "Cinnamon helps regulate blood sugar levels, fenugreek improves insulin sensitivity, and bitter gourd contains compounds that help lower blood sugar."
  },
"Stomach Pain": {
    "remedy": "Peppermint Tea, Ginger, Ajwain (Carom Seeds)",
    "preparation": "Brew peppermint tea by steeping fresh leaves or tea bags in hot water and drink 2-3 times a day. Chew small pieces of fresh ginger or drink ginger tea. Roast 1/2 teaspoon of ajwain and consume it with a pinch of black salt.",
    "use": "Peppermint relaxes stomach muscles, ginger reduces inflammation and soothes the digestive system, and ajwain relieves gas and indigestion, reducing stomach pain."
  },
  "Acidity": {
    "remedy": "Cold Milk, Fennel Seeds, Baking Soda",
    "preparation": "Drink a glass of cold milk when you feel symptoms of acidity. Chew a teaspoon of fennel seeds after meals. Mix 1/2 teaspoon of baking soda in a glass of water and drink it for quick relief.",
    "use": "Cold milk neutralizes stomach acid, fennel seeds soothe the digestive tract, and baking soda acts as an antacid to reduce acidity."
  },
  "Headache": {
    "remedy": "Peppermint Oil, Ginger Tea, Lavender Oil",
    "preparation": "Apply a few drops of peppermint oil to the temples and massage gently. Drink ginger tea made by boiling fresh ginger slices in water. Inhale the aroma of lavender oil or apply it to the temples.",
    "use": "Peppermint oil relaxes muscles and improves circulation, ginger reduces inflammation, and lavender oil helps relieve tension headaches."
  },
"Joint Pain": {
    "remedy": "Turmeric, Epsom Salt, Ginger",
    "preparation": "Mix 1/2 teaspoon of turmeric in warm milk and drink daily. Add Epsom salt to warm bath water and soak the affected joints. Drink ginger tea twice a day.",
    "use": "Turmeric has anti-inflammatory properties, Epsom salt reduces swelling, and ginger helps with pain relief."
  },
"Anxiety": {
    "remedy": "Chamomile Tea, Ashwagandha, Deep Breathing",
    "preparation": "Drink chamomile tea 2-3 times a day. Take ashwagandha supplements as recommended. Practice deep breathing for 10-15 minutes.",
    "use": "Chamomile helps relax the nervous system, ashwagandha reduces stress hormones, and deep breathing calms the mind and reduces anxiety."
  },
  "Back Pain": {
    "remedy": "Turmeric, Epsom Salt, Ginger",
    "preparation": "Mix 1/2 teaspoon of turmeric powder in warm milk and drink daily. Add 2 cups of Epsom salt to warm bathwater and soak for 15-20 minutes. Drink ginger tea made by boiling fresh ginger slices in water twice a day.",
    "use": "Turmeric has anti-inflammatory properties that reduce pain, Epsom salt relaxes muscles and reduces swelling, and ginger helps alleviate muscle soreness and inflammation."
  },
  "Tan": {
    "remedy": "Lemon Juice, Yogurt, Cucumber",
    "preparation": "Mix the juice of one lemon with 2 tablespoons of yogurt and apply it to the tanned areas. Leave it on for 30 minutes before rinsing off with lukewarm water. Grate half a cucumber and apply the pulp to the skin for 15-20 minutes.",
    "use": "Lemon juice acts as a natural bleaching agent, yogurt moisturizes the skin while helping to lighten tan, and cucumber soothes the skin and provides hydration."
  },
"Pimples": {
    "remedy": "Tea Tree Oil, Aloe Vera, Honey",
    "preparation": "Apply a few drops of tea tree oil directly onto the pimple using a cotton swab. Use fresh aloe vera gel as a spot treatment and leave it overnight. Mix honey with a few drops of lemon juice and apply it as a mask for 15-20 minutes.",
    "use": "Tea tree oil has antibacterial properties, aloe vera soothes inflammation, and honey helps reduce bacteria and heal the skin."
  },
"Dark Spots": {
    "remedy": "Vitamin C Serum, Apple Cider Vinegar, Papaya",
    "preparation": "Apply vitamin C serum to the affected areas daily. Mix equal parts of apple cider vinegar and water, apply to dark spots, and rinse after 10 minutes. Mash ripe papaya and apply it as a mask for 20-30 minutes.",
    "use": "Vitamin C brightens skin, apple cider vinegar helps lighten dark spots, and papaya contains enzymes that exfoliate and rejuvenate the skin."
  },
"Hair Fall": {
    "remedy": "Coconut Oil, Amla, Fenugreek Seeds",
    "preparation": "Warm 2 tablespoons of coconut oil and massage it into the scalp, leave it for at least 30 minutes before washing. Soak 2 tablespoons of amla overnight, grind it to a paste, and apply to the hair for 30 minutes before rinsing. Soak fenugreek seeds overnight, grind to a paste, and apply to the scalp for 30 minutes.",
    "use": "Coconut oil nourishes hair, amla strengthens hair follicles, and fenugreek seeds promote hair growth."
  },
"Hair Thinning": {
    "remedy": "Onion Juice, Olive Oil, Castor Oil",
    "preparation": "Extract onion juice and apply it to the scalp, leaving it on for 30-60 minutes before washing. Mix equal parts of olive oil and castor oil, warm slightly, and massage into the scalp. Leave it overnight and wash in the morning.",
    "use": "Onion juice promotes hair growth due to sulfur content, olive oil adds moisture, and castor oil nourishes and strengthens hair."
  },
"Laziness": {
    "remedy": "Ginger Tea, Green Tea, Honey",
    "preparation": "Brew ginger tea by boiling fresh ginger slices in water and drink it in the morning. Drink 1-2 cups of green tea daily. Mix honey with warm water and consume it in the morning.",
    "use": "Ginger tea boosts energy levels, green tea enhances metabolism, and honey provides natural energy."
  },
"Period Cramps": {
    "remedy": "Ginger Tea, Heating Pad, Chamomile Tea",
    "preparation": "Brew ginger tea by boiling fresh ginger slices and drink it several times a day. Use a heating pad on the abdomen for relief. Brew chamomile tea and drink it before bed.",
    "use": "Ginger has anti-inflammatory properties, a heating pad relaxes muscles, and chamomile tea helps ease cramps and promote relaxation."
  },
"Skin Allergy": {
    "remedy": "Oatmeal Bath, Aloe Vera, Honey",
    "preparation": "Add colloidal oatmeal to warm bathwater and soak for 15-20 minutes. Apply fresh aloe vera gel to the affected areas. Mix honey with a few drops of lemon juice and apply as a mask.",
    "use": "Oatmeal soothes irritated skin, aloe vera provides relief and hydration, and honey has antibacterial properties."
  },
"Fat Burning": {
    "remedy": "Green Tea, Apple Cider Vinegar, Lemon Water",
    "preparation": "Drink 2-3 cups of green tea daily. Mix 1-2 tablespoons of apple cider vinegar in a glass of water and drink it before meals. Squeeze the juice of half a lemon in warm water and drink it every morning.",
    "use": "Green tea boosts metabolism, apple cider vinegar helps control appetite, and lemon water aids digestion and detoxification."
  }







    # Add other remedies as necessary...
}

# Function to get remedy based on the question
def get_remedy(question):
    for key in remedies_data.keys():
        if key.lower() in question.lower():
            return remedies_data[key]
    return {"remedy": "No remedy found", "preparation": "", "use": ""}

# Define a route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for the chatbot page
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Define a route to get remedy based on user input
@app.route('/get_remedy', methods=['POST'])
def get_remedy_api():
    data = request.json
    question = data.get('question', '')
    remedy_info = get_remedy(question)
    return jsonify(remedy_info)

""" if __name__ == "__main__":
    app.run(debug=True)
 """