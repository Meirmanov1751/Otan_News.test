from fastapi import APIRouter, HTTPException
from typing import List, Dict

router = APIRouter()

# Класс категорий
class CATEGORYS:
    NEWS = 'News'
    POLICY = 'Policy'
    SOCIETY = 'Society'
    ADVERTISING = 'Advertising'
    BY_EAR = 'By hearing'

    CATEGORY_CHOICES = (
        (NEWS, 'News'),
        (POLICY, 'Policy'),
        (SOCIETY, 'Society'),
        (ADVERTISING, 'Advertising'),
        (BY_EAR, 'By hearing'),
    )

# Класс подкатегорий
class SUBCATEGORYS:
    KAZAKHSTAN_NEWS = 'Kazakhstan News'
    MANGYSTAU_NEWS = 'Mangystau News'
    WORLD_NEWS = 'World News'
    PRESIDENT = 'President'
    MEETINGS = 'Meetings'
    ECONOMY = 'Economy'
    SPORT = 'Sport'
    ECOLOGY = 'Ecology'
    MEDICINE = 'Medicine'
    EDUCATION = 'Education'
    CULTURE = 'Culture'
    TRUTH = 'Truth'
    YOUTH = 'Youth'

    SUBCATEGORY_CHOICES = (
        (KAZAKHSTAN_NEWS, 'Kazakhstan News'),
        (MANGYSTAU_NEWS, 'Mangystau News'),
        (WORLD_NEWS, 'World News'),
        (PRESIDENT, 'President'),
        (MEETINGS, 'Meetings'),
        (ECONOMY, 'Economy'),
        (SPORT, 'Sport'),
        (ECOLOGY, 'Ecology'),
        (MEDICINE, 'Medicine'),
        (EDUCATION, 'Education'),
        (CULTURE, 'Culture'),
        (TRUTH, 'Truth'),
        (YOUTH, 'Youth'),
    )

# Связь категорий и подкатегорий
CATEGORY_SUBCATEGORY_MAP = {
    CATEGORYS.NEWS: [
        SUBCATEGORYS.KAZAKHSTAN_NEWS,
        SUBCATEGORYS.MANGYSTAU_NEWS,
        SUBCATEGORYS.WORLD_NEWS,
    ],
    CATEGORYS.POLICY: [
        SUBCATEGORYS.PRESIDENT,
        SUBCATEGORYS.MEETINGS,
        SUBCATEGORYS.ECONOMY,
    ],
    CATEGORYS.SOCIETY: [
        SUBCATEGORYS.SPORT,
        SUBCATEGORYS.ECOLOGY,
        SUBCATEGORYS.MEDICINE,
        SUBCATEGORYS.EDUCATION,
        SUBCATEGORYS.CULTURE,
        SUBCATEGORYS.TRUTH,
        SUBCATEGORYS.YOUTH,
    ],
    CATEGORYS.ADVERTISING: [],
    CATEGORYS.BY_EAR: [],
}

# Словарь для быстрого доступа к названию подкатегорий
SUBCATEGORY_NAME_MAP = dict(SUBCATEGORYS.SUBCATEGORY_CHOICES)

# Endpoint для получения списка категорий
@router.get("/", response_model=List)
async def list_categories():
    # Формируем список категорий с их идентификаторами и названиями
    categories = [{"id": index + 1, "name": cat[1]} for index, cat in enumerate(CATEGORYS.CATEGORY_CHOICES)]
    return categories

# Endpoint для получения подкатегорий по ID категории
@router.get("/{category_id}/subcategories", response_model=List)
async def list_subcategories(category_id: int):
    # Проверяем, что категория существует (теперь от 1 до длины CATEGORY_CHOICES включительно)
    if category_id < 1 or category_id > len(CATEGORYS.CATEGORY_CHOICES):
        raise HTTPException(status_code=404, detail="Category not found")

    # Получаем идентификатор категории (уменьшаем на 1, чтобы получить индекс)
    category_key = CATEGORYS.CATEGORY_CHOICES[category_id - 1][0]

    # Получаем подкатегории для данной категории
    subcategories = CATEGORY_SUBCATEGORY_MAP.get(category_key, [])

    # Формируем список подкатегорий с их идентификаторами и названиями
    subcategory_list = [{"id": index + 1, "name": SUBCATEGORY_NAME_MAP[subcat]} for index, subcat in enumerate(subcategories)]

    return subcategory_list
