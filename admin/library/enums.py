from common.enums import CustomEnum


class GenreEnum(CustomEnum):

    ACTION = "Action"
    ADVENTURE = "Adventure"
    ANIMATION = "Animation"
    BIOGRAPHY = "Biography"
    COMEDY = "Comedy"
    CRIME = "Crime"
    DRAMA = "Drama"
    FAMILY = "Family"
    FANTASY = "Fantasy"
    HISTORY = "History"
    HORROR = "Horror"
    MUSIC = "Music"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    SCIENCE_FICTION = "Science Fiction"
    THRILLER = "Thriller"
    WAR = "War"
    WESTERN = "Western"


class LanguageEnum(CustomEnum):
    ENGLISH = "English"
    HINDI = "Hindi"
    MARATHI = "Marathi"
    TAMIL = "Tamil"
    TELUGU = "Telugu"
    KANNADA = "Kannada"
    MALAYALAM = "Malayalam"
    BENGALI = "Bengali"
    GUJARATI = "Gujarati"
    PUNJABI = "Punjabi"
    URDU = "Urdu"
    OTHER = "Other"

class SubCategoryEnum(CustomEnum):
    FICTION = "Fiction"
    NON_FICTION = "Non-fiction"
    POETRY = "Poetry"
    DRAMA = "Drama"
    COMICS = "Comics"
    JOURNALS = "Journals"
    MAGAZINES = "Magazines"
    NEWSPAPERS = "Newspapers"
    OTHER = "Other"


class PublisherEnum(CustomEnum):
    PENGUIN_RANDOM_HOUSE = "Penguin Random House"
    HARPER_COLLINS = "HarperCollins"
    SIMON_AND_SCHUSTER = "Simon & Schuster"
    MACMILLAN = "Macmillan"
    VILLAGE = "Village"
    CREATIVE = "Creative"
    OTHER = "Other"