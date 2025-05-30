import pandas as pd


##############################################################################################################
#
# 2. SaveCardCategory에 저장한 속성 들을 각 카드의 혜택들과 비교하여
#    category의 속성 별로 백분율을 저장합니다.
#
##############################################################################################################

class CalculateCardCategory:

    def __init__(self):
        self.category_data_df = None
        self.extract_categories = set()
        self.card_data_df = None
        self.file_path = "../../../static/data/result/"

    def load_card_data(self):
        try:
            # DataFrame으로 데이터 불러오기
            self.card_data_df = pd.read_csv(self.file_path + "card_db.csv")
        except FileNotFoundError:
            print("Error: 'card_db.csv' 파일을 찾을 수 없습니다.")

    def load_categorized_data(self):
        try:
            self.category_data_df = pd.read_csv(self.file_path + "categories.csv")
        except FileNotFoundError:
            print("Error: 'categories.csv' 파일을 찾을 수 없습니다.")

    def calculate_card_category(self):
        # 카테고리 딕셔너리 생성
        categories = dict(zip(self.category_data_df['category'], self.category_data_df['benefit']))

        # 카드별 속성 계산을 위한 딕셔너리 생성
        card_attributes = {category: [] for category in categories.keys()}
        card_attributes['card_id'] = []

        # 카드별 카테고리 속성 계산
        for index, row in self.card_data_df.iterrows():
            card_id = index
            card_categories = row[['card_category', 'card_top_category']].dropna().values

            # 각 카테고리 별로 카드에 포함된 키워드를 중복없이 카운트
            category_counts = {category: 0 for category in categories.keys()}
            for category, benefit in categories.items():
                for card_category in card_categories:
                    for cat in card_category.split(','):
                        if cat.strip() in benefit:
                            category_counts[category] += 1

            # 카드 카테고리 속성 계산
            total_count = sum(category_counts.values())
            for category, count in category_counts.items():
                total_benefit = count / total_count if total_count != 0 else 0  # 0으로 나누는 경우 방지
                card_attributes[category].append(total_benefit)

            card_attributes['card_id'].append(card_id)

        # DataFrame으로 변환
        card_attributes_df = pd.DataFrame(card_attributes)

        return card_attributes_df

if __name__ == '__main__':
    set_card_category = CalculateCardCategory()

    # load category and card data
    set_card_category.load_card_data()
    set_card_category.load_categorized_data()

    # calculate category percentage for each card
    card_attributes_df = set_card_category.calculate_card_category()

    # save card (only category and the index)
    card_attributes_df.to_csv(set_card_category.file_path + 'calculate_card_category.csv', index=False, encoding="utf-8")
    card_attributes_df.to_excel(set_card_category.file_path + 'calculate_card_category.xlsx', index=False)

    merged_df = pd.merge(set_card_category.card_data_df, card_attributes_df, on='card_name')

    # save card (with category and the card columns)
    merged_df.to_csv(set_card_category.file_path + 'final_card_data.csv', index=False, encoding="utf-8")
    merged_df.to_excel(set_card_category.file_path + 'final_card_data_view.xlsx', index=False)