################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
C:/Users/13410/Desktop/study/Summer\ Project\ Year\ 1/STEVAL_SPIN3201_example/Src/system_stm32f0xx.c 

OBJS += \
./Drivers/CMSIS/system_stm32f0xx.o 

C_DEPS += \
./Drivers/CMSIS/system_stm32f0xx.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/CMSIS/system_stm32f0xx.o: C:/Users/13410/Desktop/study/Summer\ Project\ Year\ 1/STEVAL_SPIN3201_example/Src/system_stm32f0xx.c Drivers/CMSIS/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m0 -std=gnu11 -g3 -DDEBUG -DARM_MATH_CM0 -DUSE_FULL_LL_DRIVER -DUSE_HAL_DRIVER -DSTM32F031x6 -c -I../../Inc -I../../Drivers/STM32F0xx_HAL_Driver/Inc -I../../Drivers/STM32F0xx_HAL_Driver/Inc/Legacy -I../../MCSDK_v6.1.2-Full/MotorControl/MCSDK/MCLib/Any/Inc -I../../MCSDK_v6.1.2-Full/MotorControl/MCSDK/MCLib/F0xx/Inc -I../../Drivers/CMSIS/Device/ST/STM32F0xx/Include -I../../Drivers/CMSIS/Include -I../../Drivers/CMSIS/DSP/Include -Ofast -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"Drivers/CMSIS/system_stm32f0xx.d" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Drivers-2f-CMSIS

clean-Drivers-2f-CMSIS:
	-$(RM) ./Drivers/CMSIS/system_stm32f0xx.cyclo ./Drivers/CMSIS/system_stm32f0xx.d ./Drivers/CMSIS/system_stm32f0xx.o ./Drivers/CMSIS/system_stm32f0xx.su

.PHONY: clean-Drivers-2f-CMSIS

