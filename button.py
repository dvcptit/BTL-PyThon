class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image #Lay hinh bao ngoai khối nếu có
		self.x_pos = pos[0] #Vi tri x
		self.y_pos = pos[1]#Vi tri y
		self.font = font #font chữ
		self.base_color, self.hovering_color = base_color, hovering_color  #Màu cơ bản và màu khi di chuột qua
		self.text_input = text_input # Nội dung đọan văn bản
		self.text = self.font.render(self.text_input, True, self.base_color) #Gán
		if self.image is None: #Nếu ko có hinh ảnh
			self.image = self.text # thì là khối chữ
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #Lấy vị trí trung tâm
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):#update
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):#Kiem tra có di chuột qua ko
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			#trái phải và trên dưới
			return True
		return False

	def changeColor(self, position): #đổi màu khi di chuọt qua
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)