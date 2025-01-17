from rpft.parsers.creation.datarowmodel import DataRowModel
from rpft.parsers.common.rowparser import ParserModel
from typing import List

###################################################################
class IntroductionBlockModel(ParserModel):
	msg_list: List[str] = []

class ImportanceBlockModel(ParserModel):
	msg_list: List[str] = []

class QuizContentModel(ParserModel):
	question: List[str] = []
	image: str = ''
	values: List[str] = []
	answer: str = ''
	feedback_correct: List[str] = []
	feedback_incorrect: List[str] = []

class QuizBlockModel(ParserModel):
	intro: str = ''
	content: List[QuizContentModel] = []

class TipModel(ParserModel):
	text: List[str] = []
	image: str = ''

class TipsBlockModel(ParserModel):
	intro: str = ''
	next_button: str = ''
	message: List[TipModel] = []

class ComicBlockModel(ParserModel):
	intro: str = ''
	file_name: str = ''
	n_attachments: str = ''
	next_button: str = ''
	text: List[str] = []

class HomeActivityBlockModel(ParserModel):
	intro: List[str] = []
	activity: str = ''
	positive_msg: str = ''
	negative_msg: str = ''

class CongratulationsBlockModel(ParserModel):
	msg_list: List[str] = []


class VideoBlockModel(ParserModel):
	script: str = ''
	message: str = ''
	file_name: str = ''
	expiration_time_min: str = ''


class AudioBlockModel(ParserModel):
	message: str = ''
	file_name: str = ''
	expiration_time_min: str = ''

class PlhContentModel(DataRowModel):
	module_name: str = ''
	introduction: IntroductionBlockModel = IntroductionBlockModel()
	importance: ImportanceBlockModel = ImportanceBlockModel()
	quiz: QuizBlockModel = QuizBlockModel()
	tips: TipsBlockModel = TipsBlockModel()
	comic: ComicBlockModel = ComicBlockModel()
	home_activity: HomeActivityBlockModel = HomeActivityBlockModel()
	video: VideoBlockModel = VideoBlockModel()
	audio: AudioBlockModel = AudioBlockModel()
	congratulations: CongratulationsBlockModel = CongratulationsBlockModel()


class TrackerInfoModel(ParserModel):
	name: str = ''
	tracker_tot: str = ''
	has_tracker: str = ''

class FlowStructureModel(DataRowModel):
	block: List[TrackerInfoModel] = []


class BlockMetadataModel(DataRowModel):
	include_if_cond: str = ''
	args: str = ''


#######
##demo
class ShortDemoModel(DataRowModel):
	onb_qst: List[str] = []

#########################################################
##goal check in

class TroubleModel(ParserModel):
	pb: str = ''
	tip: List[str] = []

class TroubleshootingModel(DataRowModel):
	question: str = ''
	problems: List[TroubleModel] = []

class GoalCheckInResponseModel(DataRowModel):
	pre_goal_positive: str = ''
	pre_goal_negative: str = ''
	post_goal_improved_positive: str = ''
	post_goal_improved_negative: str = ''
	post_goal_static_positive: str = ''
	post_goal_static_negative: str = ''
	post_goal_worsened_positive: str = ''
	post_goal_worsened_negative: str = ''

class GoalCheckInModel(DataRowModel):
	intro_pre_goal: str = ''
	intro_post_goal: str = ''
	pre_question: str = ''
	question: str = ''
	options: List[str] = []
	add_qr: str = ''
	negative: List[str] = []
	positive: List[str] = []
	improvement: str = ''
	response: GoalCheckInResponseModel = GoalCheckInResponseModel()
	troubleshooting: TroubleshootingModel = TroubleshootingModel()
	conclusion: str = ''

class PbSurveyBehaveModel(ParserModel):
	name: str = ''
	post_goal_msg: str = ''

class SurveyBehaveModel(DataRowModel):
	intro: str = ''
	select_instructions: str = ''
	pb: List[PbSurveyBehaveModel] = []
###########################################################
# onboarding

class OnboardingStepsModel(DataRowModel):
	flow: str = ''
	variable: str = ''

class OnboardingQuestionOptionModel(ParserModel):
	text: str = ''
	value: str = ''
	alias: str = ''

class OnboardingQuestionWithOptionsModel(DataRowModel):
	question: str = ''
	image: str = ''
	variable: str = ''
	options : List[OnboardingQuestionOptionModel] = []

class OnboardingQuestionInputTestModel(ParserModel):
	expression: str = ''
	value: str = ''
	condition_type: str = ''

class OnboardingQuestionInputModel(DataRowModel):
	question: str = ''
	variable: str = ''
	test: OnboardingQuestionInputTestModel = OnboardingQuestionInputTestModel()
	error_message: str = ''

class OnboardingRangeModel(ParserModel):
	limit: str = ''
	var_value: str = ''

class OnboardingQuestionRangeModel(DataRowModel):
	question: str = ''
	variable: str = ''
	grouping_variable: str = ''
	lower_bound: int = 0
	low_error_msg: str = ''
	upper_bound: int = 0
	up_error_msg: str = ''
	general_error_msg: str = ''
	ranges: List[OnboardingRangeModel] = []

################################
## LTP activity
class LtpActivityModel (DataRowModel):
	name: str = ''
	text: str = ''
	act_type: List[str] = ["Active"] #???
	act_age: List[int] = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17] 
	use_in_demo: str = ''
################################
## home activity check-in

class HomeActivityCheckInModel(DataRowModel):
	activity: str = ''
	positive_message: str = ''
	negative_message: str = ''

class WhatsappTemplateModel(DataRowModel):
	name: str = ''
	uuid: str = ''
	text: str = ''

#########################
## dev assessment tools
class WgUnicefModel(DataRowModel):
	intro: str = ''
	end_message_concerning: List[str] = []
	end_message_not_concerning: List[str] = []
	questions_ids: List[str] = []

class WgUnicefQuestionModel(DataRowModel):
	qst: str = ''
	options: List[str] = []
	concerning_options: List[str] = []
	concerning_feedback: str = ''

class SwycModel(DataRowModel):
	intro: List[str] = []
	options: List[str] = []
	scores: List[int] = []
	threshold_age: List[int] = []
	threshold_score: List[int] = []
	end_message_concerning: List[str] = []
	end_message_not_concerning: List[str] = []
	questions: List[str] = []

#########################
## delivery

class GoalModel(DataRowModel):
	goal_name: str = ''
	priority: str = ''
	age_group: str = ''
	relationship: str = ''
	modules: List[str] = []



class SplitModel(DataRowModel):
	split_variable: str = ''
	flow_name: str = ''
	text_name: str = ''


class ModuleModel(DataRowModel):
	module_name: str = ''
	age_baby: bool = True
	age_child: bool = True
	age_teen: bool = True

class HandlerWrapperModel(DataRowModel):
	pre_update_flow: str = ''
	handler_flow: str = ''
	post_update_flow: str = ''

class OptionsWrapperOneOptionModel(ParserModel):
	message: str = ''
	question: str = ''
	affirmative: str = ''
	negative: str = ''
	no_message: str = ''

class OptionsWrapperNoOptionModel(ParserModel):
	message: str = ''
	image: str = ''

class OptionsWrapperModel(DataRowModel):
	list_var: str = ''
	dict_var: str = ''
	dict_ID: str = ''
	n_max_opt: int = 9
	msg_no_options: OptionsWrapperNoOptionModel = OptionsWrapperNoOptionModel()
	msg_one_option: OptionsWrapperOneOptionModel = OptionsWrapperOneOptionModel()
	msg_multiple_options: str = ''
	extra_option: str = ''
	extra_message: str = ''
	update_var: str = ''
	update_var_flow: str = ''


class ProceedModel(ParserModel):
	question: str = ''
	yes_opt: str = ''
	no_opt: str = ''
	no_msg: str = ''


class SelectGoalModel(DataRowModel):
	update_prog_var_flow: str = ''
	split_by_goal_update_flow: str = ''
	goal_description: str = ''	
	proceed: ProceedModel = ProceedModel()

class InteractionOptionModel(ParserModel):
	text: str = ''
	proceed_result_value: str = ''
	stop_message: str = ''

class InteractionModel(DataRowModel):
	question: str = ''
	options: List[InteractionOptionModel] = []
	wa_template_ID: str = ''
	wa_template_vars: List[str] = []



class TimedProgrammeModel(DataRowModel):
	completion_variable: str = ''
	incomplete_value: str = ''
	incomplete_test: str = ''
	incomplete_name: str = ''
	interaction_flow: str = ''
	interaction_proceed_value: str = ''
	flow: str = ''


class ActivityTypeModel(DataRowModel):
	option_name: str = ''

class ActivityOfferModel(DataRowModel):
	activity_handler_flow: str = ''
	offer_msg: str = ''
	accept: str = ''
	refuse: str = ''
	refuse_msg: str = ''
	next_offer_msg: str = ''
	next_accept: str = ''
	next_refuse: str = ''
	next_refuse_msg: str = ''
	next_refuse_flow: str = ''
	next_other_opt: str = ''
	next_other_msg: str = ''
	next_other_flow: str = ''

class ComicNamesModel(DataRowModel):
	names: List[str] = []

class DictionaryModel(DataRowModel):
	languages: List[str] = []

class UseDictionaryModel(DataRowModel):
	dict_name: str = ''
	N: str = ''
	key: str = ''

####################################
## Menu
class MenuOptionModel(ParserModel):
	text: str = ''
	flow: str = ''
	
class MessageMenuModel(ParserModel):
	text: str = ''
	image: str = ''
	
class ReturnOptionModel(ParserModel):
	text: str = ''
	flow: str = ''

class MenuModel(DataRowModel):
	message: MessageMenuModel = MessageMenuModel()
	return_option: ReturnOptionModel = ReturnOptionModel()
	options: List[MenuOptionModel] = []

class MenuBlocksModel(ParserModel):
	no_opt: str = ''
	one_opt: str = ''
	mult_opt: str = ''

class MenuProgressModel(DataRowModel):
	show_options_id: str = ''
	menu_blocks: MenuBlocksModel = MenuBlocksModel()

class SelectGoalMenuModel(DataRowModel):
	type: str = ''

class MissingProfileModel(ParserModel):
	msg: str = ''
	value: str = ''	

class VarProfileModel(ParserModel):
	val: str = ''
	alias: str = ''
	
class SettingsProfileModel(DataRowModel):
	current_info_msg: str = ''
	missing: MissingProfileModel = MissingProfileModel()
	update_inquiry: str = ''
	update_var_flow: str = ''
	confirmation_msg: str = ''
	update_prog_var_flow: str = ''
	variable: str = ''
	var: List[VarProfileModel] = []
											
####################################
## Safeguarding

class ReferralsModel(DataRowModel):
	referrals: str = ''


class SafeguardingRedirectModel(DataRowModel):
	flow: str = ''
	expiration_msg: str = ''
	kw_type: str = ''
	proceed: str = ''

class SafeguardingEntryModel(DataRowModel):
	question: str = ''
	intro: str = ''
	no_message: str = ''